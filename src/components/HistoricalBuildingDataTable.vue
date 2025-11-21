<template>
  <div class="historical-table-cont">
    <table class="historical-data">
      <thead>
        <tr>
          <th scope="col">Year</th>

          <th class="text-center grade-header -overall">
            Overall <br />
            Grade
          </th>
          <th class="text-center grade-header small-col-header">
            Emissions <br />
            Intensity <br />
            Sub-Grade
          </th>
          <th class="text-center grade-header small-col-header">
            Energy Mix <br />
            Sub-Grade
          </th>
          <th class="text-center grade-header small-col-header">
            Reporting Mix <br />
            Sub-Grade
          </th>

          <th scope="col">
            GHG Intensity <span class="unit">kg CO<sub>2</sub>e / sqft</span>
          </th>
          <th scope="col">
            GHG Emissions <span class="unit">metric tons CO<sub>2</sub>e</span>
          </th>

          <!-- Energy Mix & Values -->
          <th class="text-center">Energy Mix</th>
          <th v-if="renderedColumns.includes('ElectricityUse')" scope="col">
            Electricity Use <span class="unit">kBTU</span>
          </th>
          <th v-if="renderedColumns.includes('NaturalGasUse')" scope="col">
            Fossil Gas Use <span class="unit">kBTU</span>
          </th>
          <th v-if="renderedColumns.includes('DistrictSteamUse')" scope="col">
            District <br />
            Steam Use <span class="unit">kBTU</span>
          </th>
          <th
            v-if="renderedColumns.includes('DistrictChilledWaterUse')"
            scope="col"
          >
            District Chilled <br />
            Water Use <span class="unit">kBTU</span>
          </th>

          <th scope="col">Source EUI <span class="unit">kBTU / sqft</span></th>
          <th v-if="renderedColumns.includes('GrossFloorArea')" scope="col">
            Floor Area <span class="unit">sqft</span>
          </th>

          <th
            v-if="renderedColumns.includes('ChicagoEnergyRating')"
            scope="col"
          >
            Chicago Energy<br />
            Rating
          </th>
          <th v-if="renderedColumns.includes('ENERGYSTARScore')" scope="col">
            Energy Star<br />
            Score
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="benchmark in historicBenchmarks"
          :key="benchmark.DataYear"
          :class="{ 'has-imputed-data': benchmark.ImputedFields && benchmark.ImputedFields !== '' }"
        >
          <td class="bold">{{ benchmark.DataYear }}</td>

          <!-- Only show any grades if the average exists for that year, otherwise it's
            incomplete data-->
          <td class="text-center">
            <LetterGrade
              v-if="benchmark.AvgPercentileLetterGrade"
              class="-overall"
              :grade="benchmark.AvgPercentileLetterGrade"
            />
          </td>
          <td class="text-center">
            <LetterGrade
              v-if="benchmark.AvgPercentileLetterGrade"
              :grade="benchmark.GHGIntensityLetterGrade"
            />
          </td>
          <td class="text-center">
            <LetterGrade
              v-if="benchmark.AvgPercentileLetterGrade"
              :grade="benchmark.EnergyMixLetterGrade"
            />
          </td>
          <td class="text-center">
            <LetterGrade
              v-if="benchmark.AvgPercentileLetterGrade"
              :grade="benchmark.SubmittedRecordsLetterGrade"
            />
          </td>

          <td :class="{ 'has-imputed-value': isFieldImputed(benchmark, 'GHGIntensity') }">
            {{ benchmark.GHGIntensity }}
            <span
              v-if="isFieldImputed(benchmark, 'GHGIntensity')"
              v-tooltip.html.left="{
                content: getImputedTooltip(benchmark, 'GHGIntensity'),
                delay: { show: 200, hide: 0 },
                offset: 16,
                popperOptions: {
                  modifiers: {
                    preventOverflow: { enabled: true },
                    hide: { enabled: false }
                  }
                }
              }"
              class="imputed-indicator"
            >
              *
            </span>
          </td>
          <td :class="{ 'has-imputed-value': isFieldImputed(benchmark, 'TotalGHGEmissions') }">
            {{ benchmark.TotalGHGEmissions | optionalFloat }}
            <span
              v-if="isFieldImputed(benchmark, 'TotalGHGEmissions')"
              v-tooltip.html.left="{
                content: getImputedTooltip(benchmark, 'TotalGHGEmissions'),
                delay: { show: 200, hide: 0 },
                offset: 16,
                popperOptions: {
                  modifiers: {
                    preventOverflow: { enabled: true },
                    hide: { enabled: false }
                  }
                }
              }"
              class="imputed-indicator"
            >
              *
            </span>
          </td>

          <!-- Energy Mix & Energy (rounded because they are big numbers) -->
          <td class="energy-mix">
            <!-- Only show energy mix data if it's a reported year -->
            <div v-if="benchmark.GHGIntensity" class="mix-text">
              <div>
                <span class="prcnt"
                  >{{ calcEnergyMix(benchmark).elecPrcnt }}%</span
                >
                <span class="label">Electricity</span>
              </div>
              <div>
                <span class="prcnt"
                  >{{ calcEnergyMix(benchmark).natGasPrcnt }}%</span
                >
                <span class="label">Fossil Gas</span>
              </div>
              <div>
                <span class="prcnt"
                  >{{ calcEnergyMix(benchmark).otherPrcnt }}%</span
                >
                <span class="label">Other</span>
              </div>
            </div>

            <PieChart
              v-if="benchmark.GHGIntensity"
              :id-prefix="'y' + benchmark.DataYear"
              :graph-data="getBreakdown(benchmark)"
              :show-labels="false"
            />
          </td>
          <td
            v-if="renderedColumns.includes('ElectricityUse')"
            :class="{ 'has-imputed-value': isFieldImputed(benchmark, 'ElectricityUse') }"
          >
            {{ benchmark.ElectricityUse | optionalInt }}
            <span
              v-if="isFieldImputed(benchmark, 'ElectricityUse')"
              v-tooltip.html.left="{
                content: getImputedTooltip(benchmark, 'ElectricityUse'),
                delay: { show: 200, hide: 0 },
                offset: 16,
                popperOptions: {
                  modifiers: {
                    preventOverflow: { enabled: true },
                    hide: { enabled: false }
                  }
                }
              }"
              class="imputed-indicator"
            >
              *
            </span>
          </td>
          <td
            v-if="renderedColumns.includes('NaturalGasUse')"
            :class="{ 'has-imputed-value': isFieldImputed(benchmark, 'NaturalGasUse') }"
          >
            {{ benchmark.NaturalGasUse | optionalInt }}
            <span
              v-if="isFieldImputed(benchmark, 'NaturalGasUse')"
              v-tooltip.html.left="{
                content: getImputedTooltip(benchmark, 'NaturalGasUse'),
                delay: { show: 200, hide: 0 },
                offset: 16,
                popperOptions: {
                  modifiers: {
                    preventOverflow: { enabled: true },
                    hide: { enabled: false }
                  }
                }
              }"
              class="imputed-indicator"
            >
              *
            </span>
          </td>
          <td
            v-if="renderedColumns.includes('DistrictSteamUse')"
            :class="{ 'has-imputed-value': isFieldImputed(benchmark, 'DistrictSteamUse') }"
          >
            {{ benchmark.DistrictSteamUse | optionalInt }}
            <span
              v-if="isFieldImputed(benchmark, 'DistrictSteamUse')"
              v-tooltip.html.left="{
                content: getImputedTooltip(benchmark, 'DistrictSteamUse'),
                delay: { show: 200, hide: 0 },
                offset: 16,
                popperOptions: {
                  modifiers: {
                    preventOverflow: { enabled: true },
                    hide: { enabled: false }
                  }
                }
              }"
              class="imputed-indicator"
            >
              *
            </span>
          </td>
          <td
            v-if="renderedColumns.includes('DistrictChilledWaterUse')"
            :class="{ 'has-imputed-value': isFieldImputed(benchmark, 'DistrictChilledWaterUse') }"
          >
            {{ benchmark.DistrictChilledWaterUse | optionalInt }}
            <span
              v-if="isFieldImputed(benchmark, 'DistrictChilledWaterUse')"
              v-tooltip.html.left="{
                content: getImputedTooltip(benchmark, 'DistrictChilledWaterUse'),
                delay: { show: 200, hide: 0 },
                offset: 16,
                popperOptions: {
                  modifiers: {
                    preventOverflow: { enabled: true },
                    hide: { enabled: false }
                  }
                }
              }"
              class="imputed-indicator"
            >
              *
            </span>
          </td>

          <td :class="{ 'has-imputed-value': isFieldImputed(benchmark, 'SourceEUI') }">
            {{ benchmark.SourceEUI }}
            <span
              v-if="isFieldImputed(benchmark, 'SourceEUI')"
              v-tooltip.html.left="{
                content: getImputedTooltip(benchmark, 'SourceEUI'),
                delay: { show: 200, hide: 0 },
                offset: 16,
                popperOptions: {
                  modifiers: {
                    preventOverflow: { enabled: true },
                    hide: { enabled: false }
                  }
                }
              }"
              class="imputed-indicator"
            >
              *
            </span>
          </td>
          <td v-if="renderedColumns.includes('GrossFloorArea')">
            {{ benchmark.GrossFloorArea | optionalInt }}
          </td>

          <td v-if="renderedColumns.includes('ChicagoEnergyRating')">
            {{ benchmark.ChicagoEnergyRating || '-' }}
          </td>
          <td v-if="renderedColumns.includes('ENERGYSTARScore')">
            {{ benchmark.ENERGYSTARScore || '-' }}
          </td>
        </tr>
      </tbody>
    </table>

    <p v-if="hasImputedData" class="imputed-legend">
      <span class="imputed-indicator">*</span> = Estimated value based on similar buildings (hover for details)
      <span class="imputed-count">{{ imputedYearsCount }} of {{ historicBenchmarks.length }} years contain estimated data</span>
    </p>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

import {
  calculateEnergyBreakdown,
  IHistoricData,
  isFieldImputed,
} from '../common-functions.vue';
import PieChart, { IPieSlice } from './graphs/PieChart.vue';
import LetterGrade from './LetterGrade.vue';

/**
 * A component that given an array of a building's benchmarking renders
 * a table showing columns of data with values (skipping any columns that
 * never had a value, like if a building never had an Energy star score)
 */
@Component({
  filters: {
    /**
     * Round and process an optional float to a locale string
     *
     * Ex: null -> '-', '12345.67' -> '12,345'
     */
    optionalInt(value: number | null) {
      if (!value) {
        return '-';
      }
      return Math.round(value).toLocaleString();
    },

    optionalFloat(value: number | null) {
      if (!value) {
        return '-';
      }
      if (value >= 1000) {
        return Math.floor(value).toLocaleString();
      }
      return value.toLocaleString();
    },
  },
  components: {
    LetterGrade,
    PieChart,
  },
})
export default class HistoricalBuildingTable extends Vue {
  @Prop({ required: true }) historicBenchmarks!: Array<IHistoricData>;

  renderedColumns: Array<string> = [];

  /** Expose isFieldImputed to template */
  isFieldImputed = isFieldImputed;

  /** Expose calculateEnergyBreakdown to template */
  getBreakdown(benchmark: IHistoricData): Array<IPieSlice> {
    return calculateEnergyBreakdown(benchmark).energyBreakdown;
  }

  /**
   * Generate tooltip content for imputed fields, including neighbor contribution data
   */
  getImputedTooltip(benchmark: IHistoricData, fieldName: string): string {
    let tooltip = '<p class="imputed-tooltip-title">This value was estimated using imputation</p>';

    // Map field names to their neighbor contribution fields
    const neighborFieldMap: { [key: string]: string } = {
      'ElectricityUse': 'NeighborsElectricityUse',
      'NaturalGasUse': 'NeighborsNaturalGasUse',
      'TotalGHGEmissions': 'NeighborsTotalGHGEmissions',
    };

    // Map field names to their corresponding data fields in neighbor objects
    const neighborValueMap: { [key: string]: { field: string, label: string, unit: string } } = {
      'ElectricityUse': { field: 'electricity_use', label: 'Electricity Use', unit: 'kBtu' },
      'NaturalGasUse': { field: 'natural_gas_use', label: 'Natural Gas Use', unit: 'kBtu' },
      'TotalGHGEmissions': { field: 'total_ghg_emissions', label: 'GHG Emissions', unit: 'Metric Tons CO2e' },
    };

    const neighborField = neighborFieldMap[fieldName];
    const valueInfo = neighborValueMap[fieldName];

    if (neighborField && benchmark[neighborField as keyof IHistoricData]) {
      const neighborDataStr = benchmark[neighborField as keyof IHistoricData] as string;

      if (neighborDataStr && neighborDataStr.trim()) {
        try {
          const neighbors = JSON.parse(neighborDataStr);

          if (Array.isArray(neighbors) && neighbors.length > 0) {
            tooltip += '<div class="imputed-tooltip-details">';
            tooltip += '<p><strong>Neighbor Buildings Used:</strong></p>';
            tooltip += '<ul class="neighbor-list">';

            // Sort by weight descending
            neighbors.sort((a: any, b: any) => (b.weight || 0) - (a.weight || 0));

            // Show top 5 neighbors
            const topNeighbors = neighbors.slice(0, 5);
            topNeighbors.forEach((neighbor: any) => {
              const weight = neighbor.weight || 0;
              const percentage = Math.round(weight * 100);
              let buildingName = neighbor.building_name || `Building ${neighbor.building_id || 'Unknown'}`;

              // Add year indicator if name is from a different year
              if (neighbor.name_from_year) {
                buildingName += ` <span class="name-year-note">(name from ${neighbor.name_from_year} records)</span>`;
              }

              const address = neighbor.address || 'Address not available';
              const propertyType = neighbor.property_type || 'Type not available';
              const sqft = neighbor.square_footage
                ? Math.round(neighbor.square_footage).toLocaleString() + ' sqft'
                : 'Size not available';

              // Get the relevant value for this field if available
              let metricValue = '';
              if (valueInfo && neighbor[valueInfo.field] !== null && neighbor[valueInfo.field] !== undefined) {
                const value = Math.round(neighbor[valueInfo.field]).toLocaleString();
                metricValue = `${valueInfo.label}: ${value} ${valueInfo.unit}`;
              }

              tooltip += `<li class="neighbor-item">`;
              tooltip += `<div class="neighbor-name">${buildingName} (${percentage}% contribution)</div>`;
              tooltip += `<div class="neighbor-details">${address}</div>`;
              tooltip += `<div class="neighbor-details">${propertyType} • ${sqft}</div>`;
              tooltip += `<div class="neighbor-details">${metricValue}</div>`;
              tooltip += `</li>`;
            });

            if (neighbors.length > 5) {
              tooltip += `<li class="more-neighbors">...and ${neighbors.length - 5} more</li>`;
            }

            tooltip += '</ul>';
            tooltip += '</div>';
          }
        } catch (e) {
          // Silent fail - tooltip will just show basic imputation message
        }
      }
    }

    return tooltip;
  }

  getRenderedColumns(): Array<string> {
    if (this.historicBenchmarks.length === 0) {
      return [];
    }
    const allColKeys = Object.keys(this.historicBenchmarks[0]) as Array<
      keyof IHistoricData
    >;
    const blankData = [null, '', 0.0, undefined];

    const notEmptyColKeys = allColKeys.filter((colKey) => {
      // A column is not empty if any of the datapoints
      // for that category are not part of our predefined
      // blank data states seen in the blankData array
      return this.historicBenchmarks.some((annualData: IHistoricData) => {
        return !blankData.includes(annualData[colKey]);
      });
    });
    return notEmptyColKeys;
  }

  calcEnergyMix(benchmarkRow: IHistoricData): {
    elecPrcnt: number;
    natGasPrcnt: number;
    otherPrcnt: number;
  } {
    const totalUse =
      benchmarkRow.ElectricityUse +
      benchmarkRow.NaturalGasUse +
      benchmarkRow.DistrictSteamUse +
      benchmarkRow.DistrictChilledWaterUse;

    const elecPrcnt = Math.round(
      100 * (benchmarkRow.ElectricityUse / totalUse),
    );
    const natGasPrcnt = Math.round(
      100 * (benchmarkRow.NaturalGasUse / totalUse),
    );
    const otherUse =
      benchmarkRow.DistrictSteamUse ||
      0 + benchmarkRow.DistrictChilledWaterUse ||
      0;
    const otherPrcnt = Math.round((100 * otherUse) / totalUse);

    return { elecPrcnt, otherPrcnt, natGasPrcnt };
  }

  /**
   * Check if any benchmark has imputed data
   */
  get hasImputedData(): boolean {
    return this.historicBenchmarks.some(
      (benchmark) => benchmark.ImputedFields && benchmark.ImputedFields !== ''
    );
  }

  /**
   * Count how many years have imputed data
   */
  get imputedYearsCount(): number {
    return this.historicBenchmarks.filter(
      (benchmark) => benchmark.ImputedFields && benchmark.ImputedFields !== ''
    ).length;
  }

  created(): void {
    this.renderedColumns = this.getRenderedColumns();
  }
}
</script>

<style lang="scss">
.historical-table-cont {
  max-width: 100%;
  overflow-x: auto;
  margin-top: 0.5rem;
  margin-bottom: 1rem;
}

table.historical-data {
  border: solid 0.125rem $grey;
  border-radius: $brd-rad-small;
  border-collapse: collapse;
  width: 100%;
  min-width: 80rem;

  .unit {
    display: block;
    font-size: 0.75rem;
    font-weight: normal;
  }

  .energy-mix {
    display: flex;
    font-size: 0.8125rem;
    align-items: center;
    justify-content: space-around;
    gap: 1rem;

    .mix-text {
      flex-basis: 6rem;

      div {
        display: flex;
        justify-content: space-between;
        gap: 0.5rem;

        .prcnt {
          width: 40%;
          text-align: right;
        }
        .label {
          width: 100%;
        }
      }
    }

    .pie-chart-cont {
      width: 4rem;
    }
  }

  th,
  td {
    padding: 0.5rem 0.5rem;
    // Numbers should be right aligned, and most columns are numbers
    text-align: right;

    &:first-of-type {
      padding-left: 0.75rem;
    }
    &.text-center {
      text-align: center;
    }
  }

  thead {
    tr {
      background-color: $grey;
    }

    th {
      line-height: 1.25;
      font-size: 0.825rem;
      white-space: nowrap;

      &.grade-header {
        width: 3rem;

        &.-overall {
          padding-left: 1rem;
        }
      }

      &.small-col-header {
        font-weight: normal;
        font-size: 0.7rem;
      }
    }
  }

  tbody tr:nth-of-type(even) {
    background-color: $grey-light;
  }

  tbody tr.has-imputed-data {
    border-left: 3px solid #ff6b6b;
  }

  td.has-imputed-value {
    background-color: rgba(255, 107, 107, 0.08);
  }

  .letter-grade {
    font-size: 1.25rem;

    &.-overall {
      font-size: 1.75rem;
    }
    &:not(.-overall) {
      vertical-align: bottom;
    }
  }

  .imputed-indicator {
    color: #ff6b6b;
    font-weight: bold;
    cursor: help;
    margin-left: 2px;
    font-size: 1rem;
    display: inline-block;
    animation: pulse-subtle 2s ease-in-out infinite;
  }

  @keyframes pulse-subtle {
    0%, 100% {
      opacity: 1;
    }
    50% {
      opacity: 0.7;
    }
  }
}

.imputed-legend {
  margin-top: 0.5rem;
  margin-bottom: 0;
  font-size: 0.875rem;
  color: #ff6b6b;
  font-style: italic;

  .imputed-indicator {
    cursor: default;
  }

  .imputed-count {
    margin-left: 1rem;
    padding-left: 1rem;
    border-left: 1px solid rgba(255, 107, 107, 0.4);
    font-weight: 500;
  }
}

// Tooltip styling for imputed value details
// Use :deep to target v-tooltip generated elements
:deep(.tooltip) {
  // Prevent tooltip from interfering with mouse events to avoid flashing
  pointer-events: none;
}

:deep(.tooltip-inner) {
  pointer-events: none;
}

.tooltip {
  .imputed-tooltip-title {
    margin: 0 0 0.5rem 0;
    font-weight: bold;
  }

  .imputed-tooltip-details {
    margin-top: 0.5rem;
    padding-top: 0.5rem;
    border-top: 1px solid rgba(255, 255, 255, 0.3);

    p {
      margin: 0.25rem 0;
      font-size: 0.875rem;
    }

    strong {
      color: rgba(255, 255, 255, 0.9);
    }

    .neighbor-list {
      list-style: none;
      padding-left: 0.5rem;
      margin: 0.25rem 0;
      font-size: 0.8125rem;

      .neighbor-item {
        margin: 0.5rem 0;
        padding: 0.5rem;
        padding-left: 0.75rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 0.25rem;
        border-left: 3px solid rgba(255, 255, 255, 0.3);

        .neighbor-name {
          font-weight: bold;
          margin-bottom: 0.25rem;
          font-size: 0.875rem;

          .name-year-note {
            font-weight: normal;
            font-size: 0.7rem;
            opacity: 0.7;
            font-style: italic;
          }
        }

        .neighbor-details {
          font-size: 0.75rem;
          opacity: 0.9;
          margin-top: 0.125rem;

          &:last-child {
            margin-top: 0.25rem;
            padding-top: 0.25rem;
            border-top: 1px solid rgba(255, 255, 255, 0.15);
            font-weight: 500;
            opacity: 1;
          }
        }
      }

      .more-neighbors {
        font-style: italic;
        opacity: 0.8;
        margin-top: 0.5rem;
        padding-left: 0;
      }
    }
  }
}
</style>
