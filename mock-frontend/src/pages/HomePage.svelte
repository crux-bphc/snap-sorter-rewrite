<script>
	let message = "Organize and find your photos effortlessly with SnapSorter.";
</script>

<main>
	<div class="container">
        <header class="title">SnapSorter</header>
        <p class="subtitle">{message}</p>
        <div class="button-group">
			<a href="http://127.0.0.1:8000/google-login" class="button">Login with Google</a>
        </div>
      </div>
</main>

<style>
	/* Container Styling */
	.container {
	  background: linear-gradient(135deg, #1e3a8a, #2563eb);
	  color: white;
	  min-height: 100vh;
	  display: flex;
	  flex-direction: column;
	  align-items: center;
	  justify-content: center;
	  padding: 20px;
	  text-align: center;
	}
  
	/* Title Styling */
	.title {
	  font-size: 3rem;
	  font-weight: 800;
	  margin-bottom: 20px;
	  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
	}
  
	/* Subtitle Styling */
	.subtitle {
	  font-size: 1.2rem;
	  color: #dbeafe;
	  margin-bottom: 30px;
	  max-width: 600px;
	  line-height: 1.6;
	}
  
	/* Button Group */
	.button-group {
	  display: flex;
	  justify-content: center;
	}
  
	/* Button Styling */
	.button {
	  padding: 12px 24px;
	  font-size: 1rem;
	  font-weight: 600;
	  color: white;
	  background-color: #3b82f6;
	  text-decoration: none;
	  border-radius: 6px;
	  transition: all 0.3s ease;
	  box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.2);
	}
  
	.button:hover {
	  background-color: #2563eb;
	  box-shadow: 4px 8px 16px rgba(0, 0, 0, 0.3);
	  transform: scale(1.05);
	}
</style>
