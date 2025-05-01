

//this should handle zip files at some point to handle the multiple pdfs
const handleDownloadPDF = async () => {
    try {
        const accessToken = await getAccessTokenSilently({
            authorizationParams: {
              audience: `https://dev-j3w5kkcgno5ahh5s.us.auth0.com/api/v2/`,
              scope: "read:current_user",
            },
          });
          const config = {
            headers: { Authorization: `Bearer ${accessToken}` }
        };
        const body={ responseType: "blob"};
        console.log(accessToken)
        const response = await axios.get(
            `http://localhost:3000/download/${filename}`,
            body,
            config
        );

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