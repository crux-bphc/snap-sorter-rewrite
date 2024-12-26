<script>
  // Function to initiate Google login flow
  const handleLogin = () => {
    // Redirect the user to the backend's google-login endpoint
    window.location.href = "http://127.0.0.1:8000/google-login";
  };
</script>

<main>
  <div class="container">
    <header class="title">Login to SnapSorter</header>
    <form class="login-form" on:submit|preventDefault={handleLogin}>
      <button type="submit" class="button">Login with Google</button>
    </form>
  </div>
</main>

<style>
  .container {
    max-width: 400px;
    margin: auto;
    padding: 20px;
    background: white;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    border-radius: 10px;
    text-align: center;
  }

  .title {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 20px;
  }

  .button {
    display: inline-block;
    padding: 10px 20px;
    background-color: #3b82f6;
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  .button:hover {
    background-color: #2563eb;
  }
</style>
