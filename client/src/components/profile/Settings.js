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
          <div className='phoneNumAndDeleteBtn'>
            <h4>My Phone Number: {phone_num}</h4>
            <button
              className='phoneNumDeleteBtn'
              onClick={(e) => handleDelete(e)}
            >
              Delete
            </button>
          </div>
        </Fragment>
      );
    } else {
      return (
        <div className='phoneNumAndDeleteBtn'>
          <h4>My Phone Number: </h4>
        </div>
      );
    }
  };

  return (
    <Fragment>
      <h1 className='defaultHeader'>ReddAlerts</h1>
      <div className='sectionBox'>
        <h2>Settings</h2>
        <div className='line' />
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
        <p>Format: (555)555-5555</p>
        <p className='smallText'>U.S. phone numbers only.</p>
      </div>
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
