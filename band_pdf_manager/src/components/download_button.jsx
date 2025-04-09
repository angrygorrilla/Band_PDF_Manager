

//this should handle zip files at some point to handle the multiple pdfs
const handleDownloadPDF = async () => {
    try {
        const filename = "output_cards.pdf"; // Match this to your server file name
        const response = await axios.get(
            `http://localhost:3000/download/${filename}`,
            { responseType: "blob" } // To handle binary data
        );

        // Create a blob and trigger download
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", filename);
        document.body.appendChild(link);
        link.click();
        link.parentNode.removeChild(link);
    } catch (error) {
        console.error("Error downloading PDF:", error.message);
    }
};