import React, { useState } from "react";
import "./Search.css";
import SearchIcon from "@material-ui/icons/Search";
import { Button } from "@material-ui/core";
import { useHistory } from "react-router-dom";
import { useStateValue } from "../stateProvider";
import { actionTypes } from "../reducer";
import ClearIcon from "@material-ui/icons/Clear";
import { useLocation } from 'react-router';


function Search({ hideButtons = false, query = "", qty}) {
  const location = useLocation();
  const [{}, dispatch] = useStateValue();
  const [input, setInput] = useState(query);
  const history = useHistory();
  const handleClear = () => { setInput("")}
  const search = (e) => {
    e.preventDefault();
    // console.log("u clicked", input);
    dispatch({
      type: actionTypes.SET_SEARCH_TERM,
      term: input,
    });
    history.push(`/search/${input}`);
  };
  return (
    <form className="search">
      <div className="search__input">
        <SearchIcon className="search__inputIcon" />
        <input value={input} onChange={(e) => setInput(e.target.value)} />
        {input!="" && <ClearIcon className="search__inputIcon" onClick={handleClear}/>}
      </div>

      {!hideButtons ? (
        <>
        <div className="search__buttons">
          <Button type="submit" onClick={search} variant="outlined">
            Haystack Search
          </Button>
          <Button variant="outlined"><a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ" className="linkn_button">I'm Feeling Lucky</a></Button>
        </div>
        <div className="search__buttons_text">
        <em>Index contains ~{qty} pages (soon to be much bigger)</em>
        </div>
        </>
      ) : (
        <div className="search__buttonsHidden">
          <Button
            className="search__buttonsHidden"
            type="submit"
            onClick={search}
            variant="outlined"
          >
            Haystack Search
          </Button>
          <Button variant="outlined" href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">I'm Feeling Lucky</Button>
        </div>
      )}
    </form>
  );
}

export default Search;
