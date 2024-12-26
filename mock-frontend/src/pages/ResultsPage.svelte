<script>
  import { onMount } from "svelte";

  let images = []; // To store image data fetched from the backend
  let errorMessage = ""; // To display errors if any
  let isLoading = true; // To manage the loading state

  // Fetch image data from the backend
  const fetchResults = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/get_user_results", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        images = Object.entries(data.images).map(([imageName, details]) => ({
          name: imageName,
          url: details.image_url,
          driveId: details.image_drive_id,
        }));
      } else {
        const error = await response.json();
        errorMessage = `Error: ${error.detail || "Failed to fetch image data"}`;
        console.error(error);
      }
    } catch (err) {
      errorMessage = "An error occurred while fetching the results.";
      console.error(err);
    } finally {
      isLoading = false; // Stop loading
    }
  };

  // Fetch data on component mount
  onMount(() => {
    fetchResults();
  });
</script>

<main>
  <header>
    <h1>Results</h1>
    <p>Here are the images based on your selections.</p>
    {#if errorMessage}
      <p class="error">{errorMessage}</p>
    {/if}
  </header>

  <section>
    {#if isLoading}
      <p>Loading results...</p>
    {:else if images.length > 0}
      <div class="gallery">
        {#each images as image}
          <div class="gallery-item">
            <img src={image.url} alt="Result Image" />
            <div class="image-details">
              <p>{image.name}</p>
              <a href={image.driveId} target="_blank">View on Drive</a>
            </div>
          </div>
        {/each}
      </div>
    {:else}
      <p>No results found.</p>
    {/if}
  </section>
</main>

<style>
  .error {
    color: red;
    font-weight: bold;
    margin-bottom: 1rem;
  }

  .gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
    margin-top: 2rem;
  }

  .gallery-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  img {
    width: 100%;
    height: 150px;
    object-fit: cover;
    border-radius: 8px;
    box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.2);
  }

  .image-details {
    margin-top: 0.5rem;
  }

  .image-details p {
    font-size: 0.9rem;
    font-weight: bold;
  }

  .image-details a {
    font-size: 0.8rem;
    color: #007bff;
    text-decoration: none;
  }

  .image-details a:hover {
    text-decoration: underline;
  }
</style>
