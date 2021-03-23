import React, { useState, useEffect } from "react";
import "./Footer.css";
import { Link } from "react-router-dom";
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';

function Footer({ home }){
  const styles = {
       marginTop: home ? 200 : 0,
  }
   return(
    <div className="footer" style={styles}>
        <Grid container spacing={0}>
        <Grid item xs={12} sm={4} className="footer_card">
          <img
          className="card_img"
          src="https://cdn.pixabay.com/photo/2014/12/21/23/53/hay-576266_960_720.png"
          alt="Haystack Logo"
        />
        <div className="card_text">Learn how haystack works.</div>
        </Grid>
        <Grid item xs={12} sm={4} className="footer_card">
          <img
          className="card_img"
          src="https://cdn.pixabay.com/photo/2014/12/21/23/53/hay-576266_960_720.png"
          alt="Haystack Logo"
        />
        <div className="card_text">Customize your haystack experience.</div>
        </Grid>
        <Grid item xs={12} sm={4} className="footer_card">
          <img
          className="card_img"
          src="https://cdn.pixabay.com/photo/2014/12/21/23/53/hay-576266_960_720.png"
          alt="Haystack Logo"
            />
            <div className="card_text">Feedback.</div>
        </Grid>
      </Grid>

        <div class="fine_text">
        <Link className="fine_text_link">&#169; DevClub 2021</Link>
        </div>
    </div>
   ) 
}


export default Footer;
