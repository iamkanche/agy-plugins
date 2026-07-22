const { test, expect } = require('@playwright/test');
const http = require('http');
const fs = require('fs');
const path = require('path');

let server;
let serverUrl;

test.beforeAll(async () => {
  server = http.createServer((req, res) => {
    // Sanitize query parameters and hashes from the request URL
    const urlPath = req.url.split('?')[0].split('#')[0];
    const relativePath = urlPath === '/' ? 'index.html' : urlPath.substring(1);
    const filePath = path.join(__dirname, '..', relativePath);
    const normalizedPath = path.normalize(filePath);

    // Prevent directory traversal attacks
    if (!normalizedPath.startsWith(path.join(__dirname, '..'))) {
      res.statusCode = 403;
      res.end('Forbidden');
      return;
    }

    fs.readFile(normalizedPath, (err, data) => {
      if (err) {
        res.statusCode = 404;
        res.end('Not Found');
      } else {
        // Set basic MIME types
        if (normalizedPath.endsWith('.html')) {
          res.setHeader('Content-Type', 'text/html');
        } else if (normalizedPath.endsWith('.css')) {
          res.setHeader('Content-Type', 'text/css');
        } else if (normalizedPath.endsWith('.js')) {
          res.setHeader('Content-Type', 'application/javascript');
        } else if (normalizedPath.endsWith('.json')) {
          res.setHeader('Content-Type', 'application/json');
        } else if (normalizedPath.endsWith('.svg')) {
          res.setHeader('Content-Type', 'image/svg+xml');
        }
        res.statusCode = 200;
        res.end(data);
      }
    });
  });

  await new Promise((resolve) => {
    server.listen(0, '127.0.0.1', () => {
      const { port } = server.address();
      serverUrl = `http://127.0.0.1:${port}`;
      resolve();
    });
  });
});

test.afterAll(async () => {
  if (server) {
    await new Promise((resolve) => server.close(resolve));
  }
});

test.describe('Antigravity Plugins Marketplace & SDD Inspector E2E Checks', () => {
  
  test('Root Dashboard - loads correctly without console errors and shows plugins', async ({ page }) => {
    const consoleErrors = [];
    page.on('console', msg => {
      if (msg.type() === 'error') consoleErrors.push(msg.text());
    });
    page.on('pageerror', err => {
      consoleErrors.push(err.message);
    });

    // Navigate to root index.html
    const response = await page.goto(`${serverUrl}/index.html`);
    expect(response.status()).toBe(200);

    // Verify Title
    await expect(page).toHaveTitle(/Antigravity Plugins Marketplace/);

    // Verify active plugin nav cards/buttons are present
    const navItems = page.locator('.plugin-nav-btn');
    await expect(navItems).toHaveCount(3); // git, gh-cli, sdd

    // Verify no JS errors occurred during load
    expect(consoleErrors).toEqual([]);

    // Verify no unexpected layout blowouts
    const overflowDetected = await page.evaluate(() => {
      return document.documentElement.scrollWidth > document.documentElement.clientWidth;
    });
    expect(overflowDetected).toBe(false);
  });

  test('SDD Inspector - loads connection map SVG and supports node selection', async ({ page }) => {
    const consoleErrors = [];
    page.on('console', msg => {
      if (msg.type() === 'error') consoleErrors.push(msg.text());
    });
    page.on('pageerror', err => {
      consoleErrors.push(err.message);
    });

    // Navigate to SDD inspector index.html
    const response = await page.goto(`${serverUrl}/plugins/sdd/index.html`);
    expect(response.status()).toBe(200);

    // Verify Title
    await expect(page).toHaveTitle(/Antigravity SDD Workflow Plugin Inspector/);

    // Verify connection map SVG exists
    const connectionMap = page.locator('#connection-map-svg');
    await expect(connectionMap).toBeVisible();

    // Verify command nodes are rendered inside the SVG
    const nodes = page.locator('#connection-map-svg [data-node-id]');
    const nodeCount = await nodes.count();
    expect(nodeCount).toBeGreaterThanOrEqual(15);

    // Click on the "/sdd:run" command node
    const runNode = page.locator('[data-node-id="/sdd:run"]');
    await expect(runNode).toBeVisible();
    
    // Perform click
    await runNode.click();

    // Verify details panel displays title /sdd:run
    const detailsTitle = page.locator('#details-header-section .details-title');
    await expect(detailsTitle).toBeVisible();
    await expect(detailsTitle).toHaveText('/sdd:run');

    // Verify no JS errors occurred during interaction
    expect(consoleErrors).toEqual([]);

    // Verify no body-level layout blowouts (clipping / overflow)
    const overflowDetected = await page.evaluate(() => {
      return document.documentElement.scrollWidth > document.documentElement.clientWidth;
    });
    expect(overflowDetected).toBe(false);
  });

});
