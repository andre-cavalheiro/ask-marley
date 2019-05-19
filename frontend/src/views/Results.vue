<template>
  <div class="container">
    <div class="result-list" v-if="foundResults" align="left">
      <SingleResult
              v-for="(res, index) in results"
              :key="index"
              :drug="res"
      />
    </div>
    <div v-else>
      No results were found
    </div>
  </div>
</template>

<script>
  import SingleResult from '@/components/SingleResult.vue'

  export default {
    name: 'results',
    data: () => {
      return {
        foundResults: true,
      }
    },
    computed: {
      results() {
        return this.$store.state.results
      },
    },
    components: {
      SingleResult
    },
  }
</script>