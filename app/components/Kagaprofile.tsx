import React from "react";
import styles from "./profile.module.css";

const Kagaprofile = () => {
    return (
      <>
        <table className={styles.profileTable}>
          <tr>
            <th>名前</th> <td>加賀 翔（かが しょう）</td>
          </tr>
          <tr>
            <th>生年月日</th> <td>1993年5月16日</td>
          </tr>
          <tr>
            <th>出身地</th> <td>岡山県備前市</td>
          </tr>
          <tr>
            <th>身長</th> <td>174cm</td>
          </tr>
          <tr>
            <th>学歴</th> <td>備前中学校卒業</td>
          </tr>
          <tr>
            <th>趣味</th> <td>自由律俳句、短歌</td>
          </tr>
          <tr>
            <th>特技</th> <td>写真撮影</td>
          </tr>
      </table>
      
      </>
    ) 
}

export default Kagaprofile