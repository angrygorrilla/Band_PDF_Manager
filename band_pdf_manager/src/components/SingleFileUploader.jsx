import React, { useState } from "react"

const SingleFileUploader = () => {
  const [file, setFile] = useState(null)
  const [status, setStatus] = useState("initial")

  const handleFileChange = e => {
    if (e.target.files) {
      setStatus("initial")
      setFile(e.target.files[0])
    }
  }

  const handleUpload = async () => {
    if (file) {
      setStatus("uploading")

      const formData = new FormData()
      formData.append("file", file)

      try {
        const result = await fetch("http://127.0.0.1:5002", {
          method: "POST",
          body: formData
        })

        const data = await result.json()

        console.log(data)
        setStatus("success")
      } catch (error) {
        console.error(error)
        setStatus("fail")
      }
    }
  }

  return (
    <>
      <div className="input-group">
        <input id="file" type="file" onChange={handleFileChange} />
      </div>
      {file && (
        <section>
          File details:
          <ul>
            <li>Name: {file.name}</li>
            <li>Type: {file.type}</li>
            <li>Size: {file.size} bytes</li>
          </ul>
        </section>
      )}

      {file && (
        <button onClick={handleUpload} className="submit">
          Upload a file
        </button>
      )}

      <Result status={status} />
    </>
  )
}

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

export default SingleFileUploader
