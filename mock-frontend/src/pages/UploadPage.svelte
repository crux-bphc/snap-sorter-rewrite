<script>
  import { onMount } from "svelte";

  let file = null;

  const checkAuthentication = () => {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("You must log in to access this page.");
      window.location.href = "#/login";
    }
  };

  onMount(() => {
    // Get the part of the hash after `#/upload`
    const hashFragment = window.location.hash.split("?")[1]; // Extract query parameters
    const urlParams = new URLSearchParams(hashFragment);

    const token = urlParams.get("token");
    console.log("Extracted Token:", token);

    if (token) {
      localStorage.setItem("token", token);
      // Clean up URL
      window.history.replaceState({}, document.title, "/#/upload");
    } else {
      alert("You must log in to access this page.");
      window.location.href = "#/login";
    }
  });

  const handleFileSelect = (event) => {
    file = event.target.files[0];
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file to upload.");
      return;
    }

    const token = localStorage.getItem("token");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();

        // Redirect based on `intermediate_confidence` field
        if (Object.keys(data.intermediate_confidence).length === 0) {
          // Redirect to ResultsPage
          window.location.href = "#/result";
        } else {
          // Save data to localStorage or state management
          localStorage.setItem("intermediateConfidence", JSON.stringify(data.intermediate_confidence));
          // Redirect to SelectPage
          window.location.href = "#/select";
        }
      } else {
        const error = await response.json();
        alert(`Error: ${error.detail || "Upload failed"}`);
      }
    } catch (err) {
      console.error(err);
      alert("An error occurred. Please try again.");
    }
  };
</script>

<main class="upload-container">
  <header>
    <h1>Upload Your Image</h1>
    <p class="description">Select an image to identify your cluster of photos.</p>
  </header>
  <div class="upload-box">
    <input
      type="file"
      id="fileInput"
      accept="image/*"
      on:change={handleFileSelect}
      class="file-input"
    />
    <label for="fileInput" class="upload-label">Choose File</label>
  </div>
  <button on:click={handleUpload} class="upload-button">Upload</button>
</main>
  
  <style>
    :global(body) {
      margin: 0;
      font-family: Arial, sans-serif;
      background-color: #f4f6f8;
      color: #333;
    }
  
    .upload-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      padding: 20px;
    }
  
    header h1 {
      font-size: 2rem;
      color: #1e3a8a;
      margin-bottom: 10px;
    }
  
    .description {
      font-size: 1rem;
      color: #64748b;
      margin-bottom: 20px;
      text-align: center;
      max-width: 600px;
    }
  
    .upload-box {
      position: relative;
      margin-bottom: 20px;
    }
  
    .file-input {
      width: 0.1px;
      height: 0.1px;
      opacity: 0;
      overflow: hidden;
      position: absolute;
      z-index: -1;
    }
  
    .upload-label {
      display: inline-block;
      cursor: pointer;
      background-color: #3b82f6;
      color: white;
      padding: 10px 20px;
      border-radius: 5px;
      transition: background-color 0.3s ease;
      font-size: 1rem;
      font-weight: bold;
    }
  
    .upload-label:hover {
      background-color: #2563eb;
    }
  
    .upload-button {
      background-color: #1e40af;
      color: white;
      padding: 10px 30px;
      border: none;
      border-radius: 5px;
      font-size: 1rem;
      font-weight: bold;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }
  
    .upload-button:hover {
      background-color: #1e3a8a;
    }
  
    .upload-button:disabled {
      background-color: #94a3b8;
      cursor: not-allowed;
    }
  </style>
  