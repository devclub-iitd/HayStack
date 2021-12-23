import React, {useState, useEffect} from "react";
import "./Home.css";
import { Link } from "react-router-dom";
import AppsIcon from "@material-ui/icons/Apps";
import { Avatar } from "@material-ui/core";
import Search from "./Search";
import logo from './LogoSVGWhiteBG.svg'
import haystack from './haystack.png'
import Footer from './Footer';

var elasticsearch = require('elasticsearch');

var client = new elasticsearch.Client({
    host: 'http://elastic:9200/' 
    // http://localhost:9200/ 
    // http://root:12345@localhost:9200/ 
    // If you have set username and password
});

function Home() {
  const [indexQty, setIndexQty] = useState();
  useEffect(() => {
    client.search({
      index: "iitd_sites", // Your index name for example crud 
      body: {
        "query": {
          "match_all": {}
        }
      }
    }).then(function (resp) {
        setIndexQty(resp['hits']['total']['value']);
    }, function (err) {
      console.log(err.message);
    });
  }, [])
  return (
    <div className="home">
      <div className="home__header">
        <div className="home__headerLeft">
          <img src={logo} alt="DevClub Logo" width="100" />
        </div>
      </div>
      <div className="home__body">
        <img
          src={haystack}
          atl=""
          height="150"
        />
        <div className="home__inputContainer">
          <Search qty={indexQty} />
        </div>
      </div>
      <Footer home/>
    </div>
  );
}

export default Home;
