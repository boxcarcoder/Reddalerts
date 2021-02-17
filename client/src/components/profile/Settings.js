import React, { Fragment, useState } from 'react';
import { submitPhoneNumber } from '../../actions/profile';

const Settings = () => {
  const [formData, setFormData] = useState({
    phoneNumber: '',
  });

  const { phoneNumber } = formData;

  const handleSubmit = (e) => {
    e.preventDefault();
    submitPhoneNumber(phoneNumber);
  };

  const handlePhoneNumber = (e) => {
    setFormData({
      ...formData,
      phoneNumber: e.target.value,
    });
  };

  return (
    <Fragment>
      <h1>ReddAlerts</h1>
      <h3>Settings</h3>
      <form onSubmit={handleSubmit}>
        <input
          type='text'
          placeholder='Phone Number'
          value={phoneNumber}
          onChange={handlePhoneNumber}
        />
        <input type='submit' value='Submit' />
      </form>
    </Fragment>
  );
};

export default Settings;
