import {FixedSizeList as List} from "react-window";
import AutoSizer from "react-virtualized-auto-sizer";
import React, { useState } from "react"

const Get_available_files_button = () => {
  const [file, setFile] = useState([])
  const [status, setStatus] = useState("initial")

  const arr = [
    ['hello','2','3']
  ];
  let AllRows = () => file.length==0?<div>no files</div>:file.map((i) => <div key = {i}>{i}</div>);

  const get_available_files = async () => {

    try {
        const result = await fetch("http://127.0.0.1:5002/file_list", {
        method: "get",
    })

    const data = await result.json()

    console.log(data)
    setFile([...data])
    console.log(file.length)

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
