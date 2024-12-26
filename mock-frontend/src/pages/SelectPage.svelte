<script>
  import { onMount } from "svelte";

  let intermediateConfidenceData = {};
  let clusters = {};
  let selectedClusters = {}; // Store user-selected clusters
  let errorMessage = "";

  // Fetch `intermediateConfidenceData` from localStorage and call the backend
  onMount(() => {
    const storedData = localStorage.getItem("intermediateConfidence");
    if (storedData) {
      intermediateConfidenceData = JSON.parse(storedData);
      fetchClusterSamples();
    } else {
      errorMessage = "No intermediate confidence data found.";
    }
  });

  // Fetch cluster samples from the backend
  const fetchClusterSamples = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/cluster_samples", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify(intermediateConfidenceData),
      });

      if (response.ok) {
        clusters = await response.json(); // Populate clusters
      } else {
        const error = await response.json();
        errorMessage = `Error: ${error.detail || "Failed to fetch cluster samples"}`;
        console.error(error);
      }
    } catch (err) {
      errorMessage = "An error occurred while fetching cluster samples.";
      console.error(err);
    }
  };

  // Handle user selection
  const toggleSelection = (day) => {
    if (selectedClusters[day]) {
      delete selectedClusters[day]; // Deselect the cluster
    } else {
      selectedClusters[day] = clusters[day]; // Select the cluster
    }
  };

  // Submit selected images to the backend
  const submitSelections = async () => {
    // Extract only the selected images into a flat array
    const selectedImages = Object.values(selectedClusters)
      .flatMap((cluster) => cluster.images)
      .filter((image) => typeof image === "string" && image.trim() !== ""); // Ensure valid strings

    console.log(selectedImages); // Debugging log

    try {
      const response = await fetch("http://127.0.0.1:8000/update_user_selected_images", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify(selectedImages), // Send only the array of images
      });

      if (response.ok) {
        window.location.href = "#/result";
      } else {
        const error = await response.json();
        errorMessage = `Error: ${error.detail || "Failed to submit selections"}`;
        console.error(error);
      }
    } catch (err) {
      errorMessage = "An error occurred while submitting selections.";
      console.error(err);
    }
  };
</script>

<main>
  <header>
    <h1>Select Images</h1>
    <p>Choose the clusters you identify with below. Multiple selections are allowed.</p>
    {#if errorMessage}
      <p class="error">{errorMessage}</p>
    {/if}
  </header>

  <section>
    {#if Object.keys(clusters).length > 0}
      {#each Object.entries(clusters) as [day, cluster]}
        <div class="cluster">
          <h2>Day {day} - Cluster {cluster.cluster}</h2>
          <label>
            <input
              type="checkbox"
              checked={selectedClusters[day] !== undefined}
              on:change={() => toggleSelection(day)}
            />
            <img
              src={cluster.sample_url}
              alt={`Day ${day}, Cluster ${cluster.cluster} sample`}
              class="image-item"
            />
          </label>
        </div>
      {/each}
      <button on:click={submitSelections}>Submit Selections</button>
    {:else}
      <p>Loading cluster samples...</p>
    {/if}
  </section>
</main>

<style>
  .error {
    color: red;
    font-weight: bold;
    margin-bottom: 1rem;
  }

  .cluster {
    margin-bottom: 1.5rem;
  }

  .image-item {
    width: 150px;
    height: 150px;
    object-fit: cover;
    border-radius: 8px;
    box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.2);
    margin-left: 0.5rem;
  }

  button {
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  button:hover {
    background-color: #0056b3;
  }
</style>
