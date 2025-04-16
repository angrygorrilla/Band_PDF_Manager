const axios = require('axios');


import {fixedSizeList as List} from "react-window";
import AutoSizer from "react-vertualized-auto-sizer";

<AutoSizer>
{({height, width}) =>(
<List
    className="List"
    height={height}
    itemCount={1000}
    itemSize={35}
    width={width}
    >
        {Row}
    </List>
)}
</AutoSizer>

server ='http://127.0.0.1:5002'
// Make a request for a user with a given ID
axios.get('/file_list')
  .then(function (response) {
    // handle success
    console.log(response);
  })
  .catch(function (error) {
    // handle error
    console.log(error);
  })
  .finally(function () {
    // always executed
  });