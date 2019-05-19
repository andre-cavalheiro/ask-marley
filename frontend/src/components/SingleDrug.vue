<template>
  <div class="result-entry container">
    <h3>{{drug.commonName}}</h3>
    <h4>Types:</h4>
    <p v-for="type in drug.types">{{type}}</p>
    <br>
    {{drug.description}}
    {{drug.linksForMoreInfo}}
  </div>
</template>

<script>
export default {
  name: 'single-drug',
  props: {
    drug: {
      required: true,
      type: Object
    },
  }
}
</script>