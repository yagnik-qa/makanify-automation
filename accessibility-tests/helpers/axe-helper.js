const { AxeBuilder } = require('@axe-core/playwright');

/**
 * Runs an Axe accessibility scan on the given Playwright Page object.
 * Prints detailed logs of any violations found and fails the test.
 * 
 * @param {import('@playwright/test').Page} page - The Playwright Page instance to scan.
 * @param {object} [options] - Custom scanning options.
 * @param {string[]} [options.tags] - List of Axe tags (e.g. ['wcag2a', 'wcag2aa', 'best-practice']).
 * @param {string[]} [options.rules] - List of specific Axe rule IDs to run.
 * @returns {Promise<void>}
 */
async function runAxeScan(page, options = {}) {
  const builder = new AxeBuilder({ page });

  // Use WCAG 2.0 & 2.1 Level A and AA tags by default if no tags or rules are specified
  const tags = options.tags || ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice'];
  builder.withTags(tags);

  if (options.rules && options.rules.length > 0) {
    builder.withRules(options.rules);
  }

  const results = await builder.analyze();
  const violations = results.violations;

  if (violations.length > 0) {
    printViolationsReport(violations, page.url());
    throw new Error(
      `Accessibility violations found: ${violations.length} rules violated. Refer to the logs above for detailed node targets.`
    );
  }
}

/**
 * Pretty prints the accessibility violations report to console.error.
 * 
 * @param {Array<object>} violations - Array of violation objects returned by Axe.
 * @param {string} url - URL of the scanned page.
 */
function printViolationsReport(violations, url) {
  console.error('\n' + '='.repeat(80));
  console.error(`ACCESSIBILITY AUDIT FAILED FOR PAGE: ${url}`);
  console.error(`Total Violations Found: ${violations.length}`);
  console.error('='.repeat(80) + '\n');

  violations.forEach((violation, index) => {
    console.error(`Violation #${index + 1} of ${violations.length}`);
    console.error(`[Rule ID]:     ${violation.id}`);
    console.error(`[Impact]:      ${violation.impact.toUpperCase()}`);
    console.error(`[Description]: ${violation.description}`);
    console.error(`[Rule Help]:   ${violation.help}`);
    console.error(`[More Info]:   ${violation.helpUrl}`);
    console.error('[Affected DOM Nodes]:');

    violation.nodes.forEach((node, nodeIndex) => {
      console.error(`  ${nodeIndex + 1}. Selector:  ${node.target.join(' > ')}`);
      console.error(`     HTML Source: ${node.html}`);
      if (node.failureSummary) {
        console.error(`     Summary:     ${node.failureSummary}`);
      }
    });

    console.error('-'.repeat(80) + '\n');
  });
}

module.exports = {
  runAxeScan,
};
