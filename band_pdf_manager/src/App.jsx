import './App.css';

import SingleFileUploader from './components/SingleFileUploader';
import Get_available_files_button from './components/Get_available_files_button';

import ItemListWindow from './components/ItemListWindow';

function App() {
  return (
    <>
      <h1>Band PDF Scanner</h1>

      <SingleFileUploader />
      <Get_available_files_button/>
      {/* <ItemListWindow/> */}
    </>
  );
}

export default App;