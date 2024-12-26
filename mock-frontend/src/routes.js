import HomePage from './pages/HomePage.svelte';
import LoginPage from './pages/LoginPage.svelte';
import UploadPage from './pages/UploadPage.svelte';
import ResultsPage from './pages/ResultsPage.svelte';
import SelectPage from './pages/SelectPage.svelte';

export const routes = {
  '/': HomePage,       // Route for the homepage
  '/login': LoginPage, // Route for the login page
  '/upload': UploadPage, // Route for the upload page
  '/result': ResultsPage, // Route for the result page
  '/select': SelectPage // Route for the select page
};
