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
      title: 'Making Sense Of Missing Data',
      meta: [
        {
          key: 'description',
          name: 'description',
          content:
            'Learn how KNN imputation helps fill in missing building energy data to provide more complete analysis of Chicago buildings.',
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

        <p class="publish-time">
          Published <time datetime="2025-12-09">Dec. 9th, 2025</time>
        </p>

        <div class="table-of-contents">
          <h2>Table Of Contents</h2>

          <ul class="-spaced">
            <li>
              <a href="#motivation">Motivation: Why Missing Data Matters</a>
            </li>
            <li>
              <a href="#the-problem"
                >The Problem: Gaps In The Benchmarking Data</a
              >
            </li>
            <li><a href="#the-solution">The Solution: KNN Imputation</a></li>
            <li><a href="#process">How KNN Imputation Works</a></li>
            <li><a href="#results">Results & Impact</a></li>
            <li><a href="#limitations">Limitations & Considerations</a></li>
          </ul>
        </div>

        <p>
          Chicago's building benchmarking data is a powerful tool for
          understanding energy use and emissions across the city. But what
          happens when buildings don't report all their data? Let's explore how
          we use KNN imputation to fill in the gaps and provide more complete
          analysis.
        </p>

        <h2 id="motivation">Motivation: Why Missing Data Matters</h2>

        <p>
          When analyzing Chicago's building energy performance, missing data
          creates several challenges:
        </p>

        <ul class="-spaced">
          <li>
            <strong>Incomplete Rankings:</strong> Buildings with missing data
            can't be properly ranked against their peers
          </li>
          <li>
            <strong>Skewed Statistics:</strong> City-wide averages and
            percentiles become less accurate when data is missing
          </li>
          <li>
            <strong>Lost Insights:</strong> We miss opportunities to understand
            trends and patterns in building performance
          </li>
        </ul>

        <p>
          Rather than simply excluding buildings with missing data, we can use
          statistical techniques to make educated estimates based on similar
          buildings.
        </p>

        <h2 id="the-problem">The Problem: Gaps In The Benchmarking Data</h2>

        <p>
          Buildings in Chicago are required to report their energy use
          annually, but not all buildings report all metrics. Common types of
          missing data include:
        </p>

        <ul class="-spaced">
          <li>Energy use by fuel type (electricity, natural gas, steam)</li>
          <li>Total greenhouse gas emissions</li>
          <li>Energy Use Intensity (EUI) metrics</li>
          <li>
            Building characteristics like year built or gross floor area
          </li>
        </ul>

        <p>
          This missing data can happen for various reasons: reporting errors,
          buildings that use unique energy sources, or incomplete energy
          metering systems.
        </p>

        <h2 id="the-solution">The Solution: KNN Imputation</h2>

        <p>
          <strong>K-Nearest Neighbors (KNN) imputation</strong> is a
          statistical technique that fills in missing values by looking at
          similar data points. The basic idea:
        </p>

        <ol class="-spaced">
          <li>
            Find the K most similar buildings (the "nearest neighbors") that
            <em>do</em> have the missing data
          </li>
          <li>
            Use the average of those neighbors' values to fill in the missing
            data
          </li>
        </ol>

        <p>
          For example, if a large office building is missing its electricity
          use data, we find other large office buildings with similar
          characteristics and use their average electricity use as an estimate.
        </p>

        <h2 id="process">How KNN Imputation Works</h2>

        <p>Our implementation of KNN imputation follows these steps:</p>

        <ol class="-spaced">
          <li>
            <strong>Identify Missing Values:</strong> Scan the dataset to find
            buildings with incomplete energy data
          </li>
          <li>
            <strong>Select Features:</strong> Choose which building
            characteristics to use for finding similar buildings (e.g., property
            type, floor area, year built)
          </li>
          <li>
            <strong>Calculate Similarity:</strong> Measure the "distance"
            between buildings based on their characteristics
          </li>
          <li>
            <strong>Find Neighbors:</strong> Identify the K most similar
            buildings that have complete data
          </li>
          <li>
            <strong>Impute Values:</strong> Calculate the average of the
            neighbors' values and fill in the missing data
          </li>
          <li>
            <strong>Validate:</strong> Check that the imputed values are
            reasonable and flag any anomalies
          </li>
        </ol>

        <h2 id="results">Results & Impact</h2>

        <p>
          Using KNN imputation on the Chicago benchmarking data has allowed us
          to:
        </p>

        <ul class="-spaced">
          <li>Increase the completeness of our dataset significantly</li>
          <li>
            Provide more accurate city-wide statistics and building rankings
          </li>
          <li>
            Identify patterns in energy use that would have been hidden by
            missing data
          </li>
          <li>
            Make the Electrify Chicago platform more useful for residents and
            policymakers
          </li>
        </ul>

        <h2 id="limitations">Limitations & Considerations</h2>

        <p>
          While KNN imputation is a powerful tool, it's important to understand
          its limitations:
        </p>

        <ul class="-spaced">
          <li>
            <strong>Estimates, Not Facts:</strong> Imputed values are educated
            guesses based on similar buildings, not actual measurements
          </li>
          <li>
            <strong>Unique Buildings:</strong> Buildings with very unusual
            characteristics may not have good "neighbors" for comparison
          </li>
          <li>
            <strong>Preserves Patterns:</strong> Imputation tends to fill in
            values that match existing patterns, which can reduce the appearance
            of outliers
          </li>
          <li>
            <strong>Transparency:</strong> We clearly mark imputed data so users
            know which values are estimates versus actual reported data
          </li>
        </ul>

        <h2>Conclusion</h2>

        <p>
          KNN imputation helps us make the most of Chicago's building energy
          data by filling in gaps intelligently. While it's not perfect, it
          provides a more complete picture of building performance across the
          city and helps identify opportunities for energy efficiency and
          decarbonization.
        </p>

        <p>
          Have feedback on our approach to missing data? Let us know by
          <a
            href="https://github.com/vkoves/electrify-chicago/issues/new"
            target="_blank"
            rel="noopener"
          >
            filing an issue on our GitHub
            <NewTabIcon />
          </a>
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
  }
}
</style>
