import React, { useState, useEffect } from "react";
import "./SearchPage.css";
import { actionTypes } from "../reducer";
import { useStateValue } from "../stateProvider";
import triggerSearch from "../search";
import { Link } from "react-router-dom";
import { useLocation } from 'react-router';
import Search from "./Search";
import logo from './LogoSVGWhiteBG.svg'
import Pagination from '@material-ui/lab/Pagination';
import Footer from './Footer';
import qs from "qs";

var elasticsearch = require('elasticsearch');

var client = new elasticsearch.Client({
    host: 'http://localhost:9200/' 
    // http://localhost:9200/ 
    // http://root:12345@localhost:9200/ 
    // If you have set username and password
});

function SearchPage({query}) {
  const [{ term, data }, dispatch] = useStateValue();
  const [page, setPage] = useState(1);
  const handleChange = (event, value) => {
    setPage(value);
    window.scrollTo(0, 0);
  };
  const location = useLocation();
  // console.log(location['pathname'].split('/')[2])
  useEffect(() => {
    client.search({
      index: "iitd_sites", // Your index name for example crud 
      body: {
        "from": (page-1)*10,
        "size": 10,
        "query": {
          "match": {
              "body": {
                  "query" : term ?? location['pathname'].split("/")[2],
              }
          }
      }
      }
    }).then(function (resp) {
      console.log(resp);
        dispatch({
          type: actionTypes.SET_RESULTS,
          data: resp,
          term: term,
        });
    }, function (err) {
      console.log(err.message);
    });
  }, [page])
  useEffect(() => {
    setPage(1);
    client.search({
      index: "iitd_sites", // Your index name for example crud 
      body: {
        "from": (page-1)*10,
        "size": 10,
        "query": {
          "match": {
              "body": {
                  "query" : term ?? location['pathname'].split("/")[2],
              }
          }
      }
      }
    }).then(function (resp) {
      console.log(resp);
        dispatch({
          type: actionTypes.SET_RESULTS,
          data: resp,
          term: term,
        });
    }, function (err) {
      console.log(err.message);
    });
  }, [term])

  return (
    <div className="searchPage">
      <div className="searchPage__header">
        <Link to="/">
          <img
            className="searchPage__logo"
            src="https://cdn.pixabay.com/photo/2014/12/21/23/53/hay-576266_960_720.png"
            alt="Haystack Logo"
          />
        </Link>
        <div className="searchPage__headerBody">
          <Search hideButtons query={term ?? location['pathname'].split("/")[2]} home={false} />
        </div>
        <img src={logo} alt="DevClub Logo" width="80" className="searchPage__logo2"/>
      </div>
      {!data && <img src="https://i.gifer.com/4V0b.gif" className ="loader" height="100"/>}
      {data && (
        <div className="searchPage__results">
          <p className="searchPage__resultCount">
            {data['hits']['total']['value']} hits for '<strong>{term ?? location['pathname'].split("/")[2]}</strong>' ({data['took']} milliseconds) ・ Couldn't find your needle? <u>Report</u>
          </p>
          {data['hits']['hits'].map((item) => (
            <div className="searchPage__result" key={item['_source']['id']}>
              <a className="searchPage__resultLink" href={item['_source']['url']}>
                {item['_source']['url']}
              </a>
              <a href={item['_source']['url']} className="searchPage__resultTitle">
              <h2><img src={`http://www.google.com/s2/favicons?domain=`+item['_source']['url']}/>{" " + item['_source']['title'].slice(7, -8)}</h2>
              </a>
              <div className="searchPage__snippet">
              {item['_source']['link_text']}
              </div>
            </div>
          ))}
        </div>
      )}
    {data && data['hits']['total']['value']>0 && <div className="pagination"><Pagination count={data['hits']['total']['value']%10===0 ? data['hits']['total']['value']/10 : parseInt(data['hits']['total']['value']/10)+1 }  page={page} onChange={handleChange}/></div>}
    <Footer />
    </div>

  );
}


export default SearchPage;
