<script>
	import { routes } from './routes';
	import Router from 'svelte-spa-router';
  </script>
  
  <main>
	<Router {routes} />
  </main>
  
  <style>
	main {
	  min-height: 100vh;
	  display: flex;
	  flex-direction: column;
	}
  </style>
  