import React from 'react';

const DashboardTable = ({ subreddit: { name, keywords } }) => {
  const displayKeywords = (keywords) => {
    return keywords.map((keyword) => <tr>{keyword}</tr>);
  };

  return (
    <table>
      <thead>
        <th colspan='2'>{name}</th>
      </thead>
      <tbody>{displayKeywords(keywords)}</tbody>
    </table>
  );
};

export default DashboardTable;
