<script>
	import '@evidence-dev/tailwind/fonts.css';
	import '../app.css';
	import { EvidenceDefaultLayout } from '@evidence-dev/core-components';
	export let data;
</script>

<EvidenceDefaultLayout {data} title="NSW DOE Data Stack in a Box">
	<slot slot="content" />
</EvidenceDefaultLayout>
