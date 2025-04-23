import './App.css';

import SingleFileUploader from './components/SingleFileUploader';
import Get_available_files_button from './components/Get_available_files_button';
import LoginButton from './components/LoginButton';
import LogoutButton from './components/Logout_Button';
import Profile from './components/Profile';
function App() {
  return (
    <>
      <Profile/>
      <h1>Band PDF Scanner</h1>
      <LoginButton/>
      <LogoutButton/>
      <SingleFileUploader />
      <Get_available_files_button/>
    </>
  );
}

export default App;

