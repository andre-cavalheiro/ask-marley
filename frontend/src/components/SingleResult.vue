<template>
  <div class="result-entry container">
    <h3>{{drug.commonName}}</h3>
    <!--<p>{{drug.description}}</p>-->
    <p>This is a description for {{drug.commonName}}</p>
  </div>
</template>

<script>
export default {
  name: 'single-result',
  props: {
    drug: {
      required: true,
      type: Object
    },
  }
}
</script>