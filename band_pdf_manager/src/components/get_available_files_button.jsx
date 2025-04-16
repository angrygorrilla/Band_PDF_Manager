import {FixedSizeList as List} from "react-window";
import AutoSizer from "react-virtualized-auto-sizer";
import React, { useState } from "react"

const Get_available_files_button = () => {
  const [file, setFile] = useState([])
  const [status, setStatus] = useState("initial")

  const arr = [
    ['hello','2','3']
  ];
  const AllRows = () => arr.map((i) => <div key = {i}>{i}</div>);

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
  
return (
    
    <>
    <button onClick={get_available_files} className="get_files">
    Get List
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
        {AllRows/* {file.length>0 ? file.map((i, index) =>(<div> <div key={index}>{i.code}</div></div>)) : (<div>hello</div>)} */}
      </List>
    )}
  </AutoSizer>
  </>
);

const Result = ({ status }) => {
  if (status === "success") {
    return <p>✅ File uploaded successfully!</p>
  } else if (status === "fail") {
    return <p>❌ File upload failed!</p>
  } else if (status === "uploading") {
    return <p>⏳ Uploading selected file...</p>
  } else {
    return null
  }
}
}
export default Get_available_files_button
