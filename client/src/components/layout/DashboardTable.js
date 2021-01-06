import React from 'react';

const DashboardTable = ({ subreddit: { subreddit_name, keywords } }) => {
  const displayKeywords = (keywords) => {
    return keywords.map((keywordObj) => <tr>{keywordObj.keyword}</tr>);
  };

  return (
    <table>
      <thead>
        <th colspan='2'>{subreddit_name}</th>
      </thead>
      <tbody>{displayKeywords(keywords)}</tbody>
    </table>
  );
};

export default DashboardTable;
