import React, { useState, useEffect } from "react";
import "./SearchPage.css";
import { actionTypes } from "../reducer";
import parse from 'html-react-parser';
import { useStateValue } from "../stateProvider";
import triggerSearch from "../search";
import { Link } from "react-router-dom";
import { useHistory } from "react-router-dom";
import { useLocation } from 'react-router';
import Search from "./Search";
import logo from './LogoSVGWhiteBG.svg'
import Pagination from '@material-ui/lab/Pagination';
import Footer from './Footer';
import qs from "qs";

import PersonIcon from "@material-ui/icons/Person";
import SearchIcon from "@material-ui/icons/Search";
import CourseIcon from "@material-ui/icons/LocalLibrary";
import ImageIcon from "@material-ui/icons/Image";

var elasticsearch = require('elasticsearch');

var client = new elasticsearch.Client({
    host: 'http://localhost:9200/' 
    // http://localhost:9200/ 
    // http://root:12345@localhost:9200/ 
    // If you have set username and password
});

function SearchPage({query, all="_active",profs="",courses="", images=""}) {
  const [{ term, data }, dispatch] = useStateValue();
  const [page, setPage] = useState(1);
  const [allActive, setAllActive] = useState(all);
  const [profsOnly, setProfsOnly] = useState(profs);
  const [coursesOnly, setCoursesOnly] = useState(courses);
  const [imagesOnly, setImagesOnly] = useState(images);
  const history = useHistory();
  const handleChange = (event, value) => {
    setPage(value);
    window.scrollTo(0, 0);
  };
  const location = useLocation();

  const queryBodyPageUpdate = {
    "from": (page-1)*10,
    "size": 10,
    "query": {
      "bool": {  
            "must" : {
              "multi_match" : {
                "query":      term ?? location['pathname'].split("/")[2],
                "fields":   profsOnly==="_active" ? [ "url^3", "body"] : coursesOnly==="_active" ? [ "url^3", "body"] :["body"],
                "fuzziness": "AUTO",
              }
            },
            "filter": {
              "regexp": {
                "url": coursesOnly==="_active" ? ".*[a-zA-Z][a-zA-Z][a-zA-Z].*[1-9][0-9][0-9]" : ".*",
              }
            }
      }
    },
    "highlight" : {
      "pre_tags" : ["<b>"],
      "post_tags" : ["</b>"],
      "fields" : {
        "body" : {}
      }
    },
    "sort" :[
        { "visits":{"order":"desc"} }
    ]
  }
  const queryBodyTermUpdate = {
    "from": (page-1)*10,
    "size": 10,
    "query": {
      "bool": {  
            "must" : {
              "multi_match" : {
                "query":      term ?? location['pathname'].split("/")[2],
                "fields":   profsOnly==="_active" ? [ "url^3", "body"] : coursesOnly==="_active" ? [ "url^3", "body"] :["body"],
                "fuzziness": "AUTO",
              }
            },
            "filter": {
              "regexp": {
                "url": coursesOnly==="_active" ? ".*[a-zA-Z][a-zA-Z][a-zA-Z].*[1-9][0-9][0-9]" : ".*",
              }
            }
      },
    },
    "highlight" : {
      "pre_tags" : ["<b>"],
      "post_tags" : ["</b>"],
      "fields" : {
        "body" : {}
      }
    },
    "sort" :[
      { "visits":{"order":"desc"} }
    ]
  }

  useEffect(() => {
    client.search({
      index: "iitd_sites", // Your index name for example crud 
      body: queryBodyPageUpdate
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
  }, [page, allActive, profsOnly, coursesOnly])

  useEffect(() => {
    setPage(1);
    client.search({
      index: "iitd_sites", // Your index name for example crud 
      body: queryBodyTermUpdate
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
  }, [term, allActive, profsOnly, coursesOnly])

  const allActiveCall = () => { 
    setAllActive("_active");
    setProfsOnly("");
    setCoursesOnly("");
    setImagesOnly("");
  }
  const profsOnlyCall = () => { 
    setAllActive("");
    setProfsOnly("_active");
    setCoursesOnly("");
    setImagesOnly("");
  }
  const coursesOnlyCall = () => { 
    setAllActive("");
    setProfsOnly("");
    setCoursesOnly("_active");
    setImagesOnly("");
  }
  const imagesOnlyCall = () => { 
    setAllActive("");
    setProfsOnly("");
    setCoursesOnly("");
    setImagesOnly("_active");
  }
  const searchImg = (e) => {
    //e.preventDefault();
    //setAllActive("_active");
    //setProfsOnly("");
    //setCoursesOnly("");
    // console.log("u clicked", input);
    dispatch({
      //type: actionTypes.SET_RESULTS,
      term: term,
    });
    history.push(`/Images/${term}`);
  }

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

      <div className="searchPage_options">
            <div className="searchPage_optionsLeft">
            <button className={'searchPage_option' + allActive} onClick={()=>allActiveCall()}>
              <SearchIcon/>
              <span>All</span>
            </button>
            <button className={'searchPage_option' + profsOnly} onClick={()=>profsOnlyCall()}>
              <PersonIcon/>
              <span>Professors</span>
            </button>
            <button className={'searchPage_option' + coursesOnly} onClick={()=>coursesOnlyCall()}>
              <CourseIcon/>
              <span>Courses</span>
            </button>
            <button className={'searchPage_option' + imagesOnly} onClick={()=>imagesOnlyCall()}>
              <ImageIcon/>
              <span>Images</span>
            </button>
            </div>
      </div>

      {!data && <img src="https://i.gifer.com/4V0b.gif" className ="loader" height="100"/>}
      {data && (
        <div className="searchPage__results">
          <p className="searchPage__resultCount">
            {data['hits']['total']['value']} hits for '<strong>{term ?? location['pathname'].split("/")[2]}</strong>' ({data['took']} milliseconds) ・ Couldn't find your needle? <u>Report</u>
          </p>        
          
           {imagesOnly==='_active'?
           data['hits']['hits'].map((item) => (
                <div className="imagePage__result" key={item['_source']['id']}>
                {/* <a className="imagePage__resultLink" href={item['_source']['url']}>
                  {item['_source']['url']}
                </a> */}
                {item['_source']['linked_images']["img"].map((image,index) => (
                  <div class="imagePage_image" key={index}>
                    <a href={item['_source']['url']}><img src={image} width="300px" height="300px"/></a>
                  </div>
                ))}
                {/* {item['_source']['url'] && <a href={item['_source']['url']} className="searchPage__resultTitle">
                <img src={item['_source']['linked_img'][1]}/>
                </a>} */}
                
                </div> 
            
            ))
           :
           data['hits']['hits'].map((item) => (
            <div className="searchPage__result" key={item['_source']['id']}>
              <a className="searchPage__resultLink" href={item['_source']['url']} onClick={() => linkClicked(item['_source'])}>
                {item['_source']['url']}
              </a>
              {item['_source']['url'] && item['_source']['title'] && <a href={item['_source']['url']} className="searchPage__resultTitle" onClick={() => linkClicked(item['_source'])}>
              <h2><img src={`http://www.google.com/s2/favicons?domain=`+item['_source']['url']}/>{" " + item['_source']['title']}</h2>
              </a>}
              {item['highlight']['body'].map((found) =>(
                  <div className="searchPage__snippet">
                  <div className="foundElement">{parse(found)}</div>
            
                  {/* <div className="foundElement" dangerouslySetInnerHTML={{__html: found}} /> */}
                  </div>
              ))}
              <div>VISITS: {item['_source']['visits']}</div>
            </div>
          ))} 
          

        </div>
      )}
    {data && data['hits']['total']['value']>0 && <div className="pagination"><Pagination count={data['hits']['total']['value']%10===0 ? data['hits']['total']['value']/10 : parseInt(data['hits']['total']['value']/10)+1 }  page={page} onChange={handleChange}/></div>}
    <Footer />
    </div>

  );
}
 
function linkClicked(item)
{
alert(item["visits"]);
client.update({
    index: "iitd_sites",
    id:item["url"],
    body: {
      doc:{
        visits:item["visits"]+1
      }
    }
});
} 


export default SearchPage;
