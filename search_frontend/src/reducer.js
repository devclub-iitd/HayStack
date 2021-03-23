export const initialState = {
    term: null,
    data: null
  };
  export const actionTypes = {
    SET_SEARCH_TERM: "SET_SEARCH_TERM",
    SET_RESULTS: "SET_RESULTS",
  };
  const reducer = (state, action) => {
    console.log(action);
  
    switch (action.type) {
      case "SET_SEARCH_TERM":
        return {
          ...state,
          term: action.term,
        };

      case "SET_RESULTS":
        return {
          ...state,
          data: action.data,
          term: action.term,
        };
  
      default:
        return state;
    }
  };
  
  export default reducer;
  