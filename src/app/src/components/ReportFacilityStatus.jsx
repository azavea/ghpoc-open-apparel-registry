import React, { useState } from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';

import Button from '@material-ui/core/Button';
import DialogTitle from '@material-ui/core/DialogTitle';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';

import DashboardActivityReportToast from './DashboardActivityReportToast';

import {
    createDashboardActivityReport,
    resetDashbooardActivityReports,
} from '../actions/dashboardActivityReports';

import { facilityDetailsPropType } from '../util/propTypes';
import { authLoginFormRoute } from '../util/constants';

const styles = Object.freeze({
    linkStyle: Object.freeze({
        display: 'inline-block',
        fontSize: '16px',
        background: 'none',
        border: 'none',
        padding: 0,
        cursor: 'pointer',
    }),
    facilityName: Object.freeze({
        padding: '5px 0 15px',
    }),
    description: Object.freeze({
        fontWeight: 'bold',
        color: 'rgb(27, 27, 26)',
        fontSize: '16px',
    }),
    dialogActionsStyles: Object.freeze({
        display: 'flex',
        justifyContent: 'space-evenly',
        alignItems: 'center',
        padding: '10px',
    }),
    dialogContainerStyles: Object.freeze({
        padding: '10px',
    }),
    dialogTextFieldStyles: Object.freeze({
        width: '100%',
        marginTop: '10px',
        minWidth: '300px',
    }),
});

function ReportFacilityStatus({
    data,
    user,
    dashboardActivityReports: { activityReports },
    submitReport,
    resetReports,
}) {
    const [showDialog, setShowDialog] = useState(false);
    const [reasonForReport, setReportReason] = useState('');

    const closeDialog = () => {
        setShowDialog(false);
        setReportReason('');
    };

    const handleSubmit = () => {
        if (!reasonForReport.length) return;
        const closureState = data.properties.is_closed ? 'OPEN' : 'CLOSED';
        submitReport({ id: data.id, reasonForReport, closureState });
        closeDialog();
    };

    const loginButton = (
        <Button
            variant="contained"
            color="primary"
            onClick={closeDialog}
            component={Link}
            to={authLoginFormRoute}
        >
            Log In
        </Button>
    );

    const dialog = (
        <Dialog
            open={showDialog}
            onClose={closeDialog}
            aria-labelledby="status-dialogue"
            aria-describedby="status-dialog-description"
            style={styles.dialogContainerStyles}
        >
            <DialogTitle id="status-dialog-title">
                {`Report facility ${
                    data.properties.is_closed ? 'reopened' : 'closed'
                }`}
                <Typography style={styles.facilityName}>
                    {data.properties.name}
                </Typography>
                <Divider />
            </DialogTitle>
            {!user ? (
                <DialogContent>
                    <DialogContentText
                        id="status-dialog-description"
                        style={styles.description}
                    >
                        {`You must be logged in to report this facility as ${
                            data.properties.is_closed ? 'reopened' : 'closed'
                        }`}
                    </DialogContentText>
                </DialogContent>
            ) : (
                <DialogContent>
                    <DialogContentText
                        id="status-dialog-description"
                        style={styles.description}
                    >
                        Please provide information the OAR team can use to
                        verify this status change.
                    </DialogContentText>
                    <TextField
                        autoFocus
                        margin="dense"
                        id="report-reason"
                        variant="outlined"
                        multiline
                        rows={4}
                        value={reasonForReport}
                        style={styles.dialogTextFieldStyles}
                        onChange={e => setReportReason(e.target.value)}
                    />
                </DialogContent>
            )}
            {!user ? (
                <DialogActions style={styles.dialogActionsStyles}>
                    {loginButton}
                </DialogActions>
            ) : (
                <DialogActions style={styles.dialogActionsStyles}>
                    <Button onClick={closeDialog}>Cancel</Button>
                    <Button
                        onClick={handleSubmit}
                        color="primary"
                        variant="contained"
                    >
                        Report
                    </Button>
                </DialogActions>
            )}
        </Dialog>
    );

    return (
        <div>
            <button
                className="link-underline small"
                style={styles.linkStyle}
                to="#"
                onClick={() => setShowDialog(true)}
                type="button"
            >
                Report facility as{' '}
                {data.properties.is_closed ? 'reopened' : 'closed'}
            </button>
            {dialog}
            <DashboardActivityReportToast
                {...activityReports}
                resetReports={resetReports}
            />
        </div>
    );
}

ReportFacilityStatus.propTypes = {
    data: facilityDetailsPropType.isRequired,
};

function mapStateToProps({
    dashboardActivityReports,
    auth: {
        user: { user },
    },
}) {
    return { dashboardActivityReports, user };
}

function mapDispatchToProps(dispatch) {
    return {
        submitReport: data => dispatch(createDashboardActivityReport(data)),
        resetReports: () => dispatch(resetDashbooardActivityReports()),
    };
}

export default connect(
    mapStateToProps,
    mapDispatchToProps,
)(ReportFacilityStatus);