<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import NewTabIcon from '~/components/NewTabIcon.vue';

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    NewTabIcon,
  },
  metaInfo() {
    return {
      title: 'Making Sense Of Missing Data: What If Chicago Enforced Penalties for Non-Compliance?',
      meta: [
        {
          key: 'description',
          name: 'description',
          content:
            'Explore how much revenue Chicago could generate and emissions it could reduce if it enforced building benchmarking penalties like New York City.',
        },
      ],
    };
  },
})
export default class MakingSenseOfMissingData extends Vue {}
</script>
<template>
  <DefaultLayout>
    <div class="missing-data-page">
      <div class="layout-constrained">
        <g-link to="/blog" class="back-link grey-link">
          <img src="/icons/arrow-back.svg" alt="" />
          Back to Blog
        </g-link>

        <h1 id="main-content" tabindex="-1">Making Sense Of Missing Data</h1>

        <h2>What If Chicago Enforced Penalties for Non-Compliance?</h2>

        <p class="publish-time">
          Published <time datetime="2025-9-12">Dec. 9th, 2025</time>
        </p>

        <div class="table-of-contents">
          <h2>Table Of Contents</h2>

          <ul class="-spaced">
            <li>
              <a href="#the-problem">The Problem: Non-Compliance Without Consequences</a>
            </li>
            <li>
              <a href="#nyc-comparison">Chicago vs. New York City: A Tale of Two Ordinances</a>
            </li>
            <li>
              <a href="#imputed-data">Estimating What's Missing</a>
            </li>
            <li><a href="#calculator">The Fine Calculator</a></li>
            <li><a href="#conclusion">What This Means for Chicago</a></li>
          </ul>
        </div>

        <p>
          A large percentage of Chicago buildings don't report their energy data without consequence. 
          Unlike New York City, which has stricter enforcement and penalizing structures, 
          Chicago's Energy Benchmarking Ordinance lacks teeth. What would happen if Chicago adopted similar penalties?
        </p>

        <h2 id="the-problem">The Problem: Non-Compliance Without Consequences</h2>

        <p>
          Our local Energy Benchmarking Ordinance requires buildings 50,000 square feet or larger to report their energy use annually. 
          The problem? Many buildings simply don't comply, and the City doesn't enforce the ordinance.
        </p>

        <p>
          As we documented in our previous blog post
          <a href="/blog/millions-in-missed-fines" target="_blank" rel="noopener">
            Millions in Missed Fines
          </a>, the lack of enforcement means buildings face little incentive to report consistently or accurately. 
          This creates several downstream problems:
        </p>

        <ul class="-spaced">
          <li>
            <strong>Incomplete Data:</strong> Large gaps in the dataset make it harder to understand citywide energy use and emissions
          </li>
          <li>
            <strong>Anomalous Reporting:</strong> Without oversight, some buildings submit clearly erroneous data (as we explore in
            <a href="/blog/how-we-grade-buildings" target="_blank" rel="noopener">
              How We Grade Buildings
            </a>)
          </li>
          <li>
            <strong>Lost Revenue:</strong> The City misses out on millions in potential fine revenue
          </li>
          <li>
            <strong>Environmental Impact:</strong> Buildings aren't accountable for the role they play 
            in reducing emissions and improving energy efficiency
          </li>
        </ul>

        <h2 id="nyc-comparison">Chicago vs. New York City: A Tale of Two Ordinances</h2>

        <p>
          New York City has taken building emissions seriously, implementing not just benchmarking requirements 
          but also emissions caps with compounding penalties. Here's how the two cities compare:
        </p>

        <div class="ordinance-comparison-table">
          <table>
            <thead>
              <tr>
                <th>Ordinance</th>
                <th>Coverage</th>
                <th>Requirements</th>
                <th>Penalties for Non-Compliance</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Chicago Energy Benchmarking</strong></td>
                <td>Buildings ≥ 50,000 sq ft</td>
                <td>Submit energy benchmarking data</td>
                <td>$100 for first violation, plus up to $25 per day</td>
              </tr>
              <tr>
                <td><strong>NYC Local Law 84 (LL84)</strong><br/>Benchmarking</td>
                <td>Buildings ≥ 25,000 sq ft</td>
                <td>Submit energy benchmarking data</td>
                <td>$500 per quarter for failure to file</td>
              </tr>
              <tr>
                <td><strong>NYC Local Law 97 (LL97)</strong><br/>Emissions Caps</td>
                <td>Buildings > 25,000 sq ft</td>
                <td>Meet GHG emissions caps and file annual emissions report</td>
                <td>
                  <ul class="penalty-list">
                    <li>$268/kCO₂e in excess emissions</li>
                    <li>$0.50/sq ft per month for late reporting</li>
                    <li>≤ $500k for false reporting</li>
                  </ul>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <p>
          The difference is clear. Chicago's penalties are minimal and rarely enforced. 
          New York's penalties are substantial and actively enforced, 
          thereby creating real financial incentives for buildings to comply and reduce emissions.
        </p>

        <h2 id="imputed-data">Estimating What's Missing</h2>

        <p>
          Since more than 10% of required Chicago buildings don't report, 
          we've created a dataset that estimates what those missing values would be 
          using K-Nearest Neighbors (KNN) imputation. 
          This statistical technique fills in missing data by finding similar buildings 
          that did report and using their values as educated estimates.
        </p>

        <p>
          For more details on how this imputation works, check out this presentation on our imputation methodology
        </p>

        <p>
          PLACEHOLDER FOR SLIDE DECK
        </p>

        <p>
          Using this complete dataset made up of actual reported data plus imputed estimates, 
          we can better explore what would happen if Chicago imposed NYC-style penalties on all buildings, 
          including those that aren't currently reporting.
        </p>

        <h2 id="calculator">The Fine Calculator</h2>

        <p>
          Use the interactive visualization below to explore how much buildings would pay in fines under different penalty scenarios. 
          Adjust the controls to see how changing the GHG emissions cap or late reporting penalties would impact buildings of different sizes.
        </p>

        <div class="calculator-placeholder">
          <p><em>[Interactive visualization will be added here]</em></p>

          <h3>Visualization:</h3>
          <ul>
            <li><strong>X-axis:</strong> Building size buckets (by sqft), split into reporting and not reporting</li>
            <li><strong>Y-axis:</strong> Total GHG
            <li><strong>Annotations:</strong> Selected caps marked by interactive control, 
            such that everything above the cap is a different color and contributes to total fines</li>
          </ul>

          <h3>Planned Controls:</h3>
          <ul>
            <li><strong>GHG Cap:</strong> Set the emissions limit (kCO₂e per square foot) at different size cohorts</li>
            <li><strong>Late Penalty:</strong> Set the fine for late or missing reports</li>
            <li><strong>Estimated Value Toggle:</strong> Include or exclude imputed data</li>
            <li><strong>Year</strong> Switch between years, can be most recent year at first</li>
          </ul>

          <h3>Annotation:</h3>
          <ul>
            <li><strong>Potential Fines:</strong> Dynamic number representing fines produced by user controls</li>
          </ul>

          <h3>Notes:</h3>
          <ul>
            <li><strong>Defaults:</strong> Current Chicago fines and current NYC fines applied to Chicago dataset</li>
          </ul>
        </div>

        <h2 id="conclusion">What This Means for Chicago</h2>

        <p>
          Enforcing building emissions penalties isn't just about revenue, it's about creating accountability and transparency. 
          New York City's approach shows what's possible.
        </p>
      </div>
    </div>
  </DefaultLayout>
</template>

<style lang="scss">
.missing-data-page {
  div.table-of-contents {
    background: $off-white;
    border-radius: $brd-rad-small;
    padding: 1rem 1.5rem;
    width: fit-content;
    margin-bottom: 1rem;

    h2 {
      margin-top: 0;
      font-size: 1.25rem;
    }

    a {
      display: block;
      font-weight: bold;
    }

    ul {
      padding-left: 1.25rem;
      margin: 0;
    }
  }

  ul.-spaced,
  ol.-spaced {
    li + li {
      margin-top: 0.5rem;
    }
  }

  // Ordinance comparison table
  .ordinance-comparison-table {
    overflow-x: auto;
    margin: 1.5rem 0;

    table {
      width: 100%;
      border-collapse: collapse;
      border: 2px solid $grey;

      th, td {
        padding: 0.75rem;
        text-align: left;
        border: 1px solid $grey;
      }

      thead {
        background-color: $grey-light;

        th {
          font-weight: bold;
        }
      }

      tbody tr:nth-child(even) {
        background-color: $off-white;
      }

      .penalty-list {
        margin: 0;
        padding-left: 1.25rem;

        li {
          margin: 0.25rem 0;
        }
      }
    }
  }

  // Calculator placeholder
  .calculator-placeholder {
    background: $off-white;
    border: 2px dashed $grey-dark;
    border-radius: $brd-rad-small;
    padding: 2rem;
    margin: 2rem 0;
    text-align: center;

    h3 {
      margin-top: 1.5rem;
      font-size: 1.125rem;
    }

    ul {
      text-align: left;
      max-width: 40rem;
      margin-left: auto;
      margin-right: auto;
    }
  }

  // Center images
  img {
    display: block;
    margin-left: auto;
    margin-right: auto;
  }

  @media (max-width: $mobile-max-width) {
    img {
      width: 100%;
    }

    .ordinance-comparison-table {
      font-size: 0.875rem;

      table {
        th, td {
          padding: 0.5rem;
        }
      }
    }
  }
}
</style>
