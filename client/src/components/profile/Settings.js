import React, { Fragment, useState } from 'react';
import { submitPhoneNumber, deletePhoneNumber } from '../../actions/auth';
import { connect } from 'react-redux';

const Settings = ({
  submitPhoneNumber,
  deletePhoneNumber,
  authState: {
    loggedInUser: { id, phone_num },
  },
}) => {
  const [formData, setFormData] = useState({
    phoneNumber: '',
  });

  const { phoneNumber } = formData;

  const handleSubmit = (e) => {
    e.preventDefault();
    submitPhoneNumber({ id, phoneNumber });
  };

  const handlePhoneNumber = (e) => {
    setFormData({
      ...formData,
      phoneNumber: e.target.value,
    });
  };

  const handleDelete = (e) => {
    e.preventDefault();
    deletePhoneNumber(id);
  };

  const displayCurrentPhoneNum = () => {
    if (phone_num) {
      return (
        <Fragment>
          <h4>My Phone Number: {phone_num}</h4>
          <button onClick={(e) => handleDelete(e)}>delete</button>
        </Fragment>
      );
    }
  };

  return (
    <Fragment>
      <h1>ReddAlerts</h1>
      <h3>Settings</h3>
      {displayCurrentPhoneNum()}
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

const mapStateToProps = (state) => ({
  authState: state.auth,
});

export default connect(mapStateToProps, {
  submitPhoneNumber,
  deletePhoneNumber,
})(Settings);
