import React from "react";
import styles from "./profile.module.css";

const Kayaprofile = () => {
    return (
      <>
        <table className={styles.profileTable}>
          <tr>
            <th>名前</th> <td>賀屋 壮也（かや そうや）</td>
          </tr>
          <tr>
            <th>生年月日</th> <td>1993年2月19日</td>
          </tr>
          <tr>
            <th>出身地</th> <td>広島県</td>
          </tr>
          <tr>
            <th>身長</th> <td>178cm</td>
          </tr>
          <tr>
            <th>学歴</th> <td>東京学芸大学卒業</td>
          </tr>
          <tr>
            <th>趣味</th> <td>動物のイラストを描く、漫画、広島カープファン、美術館巡り</td>
          </tr>
          <tr>
            <th>特技</th> <td>合唱（少年合唱団に所属していた）</td>
          </tr>
      </table>
      
      </>
    ) 
}

export default Kayaprofile