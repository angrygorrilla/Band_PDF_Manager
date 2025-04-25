import {FixedSizeList as List} from "react-window";
import AutoSizer from "react-virtualized-auto-sizer";
import React, { useState } from "react"
import axios from "axios";
import { useAuth0 } from "@auth0/auth0-react";

const Get_available_files_button = () => {
  const [file, setFile] = useState([])
  const [status, setStatus] = useState("initial")
  const { user, isAuthenticated, getAccessTokenSilently } = useAuth0();

  let AllRows = () => file.length==0?<div>no files</div>:file.map((i) => <><button id={i} key = {i} onClick ={handleDownloadPDF}>{i}</button></>);

  const handleDownloadPDF = async (event) => {
    let filename=event.target.id
    try {
        const response = await axios.get(
            `http://127.0.0.1:5002/pdf/${filename}`,
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
const get_available_files = async () => {

  try {
      const result = await fetch("http://127.0.0.1:5002/file_list", {
      method: "get",
  })

  const data = await result.json()

  console.log(data)
  setFile([...data])
  
  } catch (error) {
      console.error(error)
      setStatus("fail")
  }
}

  const get_available_files_w_auth = async () => {

    const domain = "dev-j3w5kkcgno5ahh5s.us.auth0.com";
  
      try {
        const accessToken = await getAccessTokenSilently({
          authorizationParams: {
            audience: `https://dev-j3w5kkcgno5ahh5s.us.auth0.com/api/v2/`,
            scope: "read:current_user",
          },
        });
  

        const result = await fetch("http://127.0.0.1:5002/auth_get_list", {
          method: "get",
          // headers: {
          //   Authorization: `Bearer ${accessToken}`,
          // },
        });

      const data = await result.json()
      
      console.log(result)
      setFile([...data])
    
    } catch (error) {
        console.error(error)
        setStatus("fail")
    }
  }
  
return (
    <>
    <button onClick={get_available_files} className="get_files">
    Get List
  </button> 
  <button onClick={get_available_files_w_auth} className="get_files_w_auth">
    Get List(auth)
  </button> 
  <AutoSizer>
    
    {({ height, width }) => (
      <List
        className="List"
        height={height}
        itemCount={1000}
        itemSize={35}
        width={width}
      >
        {AllRows}
      </List>
    )}
  </AutoSizer>
  </>
);

const Result = ({ file }) => {
  return file.map((i) => <div key = {i}>{i}</div>);
  }
}
export default Get_available_files_button
