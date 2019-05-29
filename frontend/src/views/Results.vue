<template>
  <div class="container">
    <h3 :id="resultListBegin">Search Results:</h3>
    <div class="result-list" v-if="foundResults" align="left">
      <SingleResult
              class="boxed"
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

<style>
    .boxed {
        border: 1px solid black ;
        outline:1px solid black;
        padding-top: 10px;
        padding-right: 30px;
        padding-bottom: 25px;
        padding-left: 80px;
    }

</style>