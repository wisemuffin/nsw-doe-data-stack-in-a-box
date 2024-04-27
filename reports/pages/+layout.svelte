<script>
	import '@evidence-dev/tailwind/fonts.css';
	import '../app.css';
	import { EvidenceDefaultLayout } from '@evidence-dev/core-components';
	export let data;
</script>

<svelte:head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-724H1YWVH7"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-724H1YWVH7');
  </script>
</svelte:head>


<EvidenceDefaultLayout {data} title="NSW DOE Data Stack in a Box">
	<slot slot="content" />
</EvidenceDefaultLayout>
