import React from 'react';
import { string } from 'prop-types';
import SvgIcon from '@material-ui/core/SvgIcon';

export default function BadgeUnclaimed({ color }) {
    return (
        <SvgIcon viewBox="0 0 22 24">
            <path
                fill={color}
                d="M10.1520833,23.2970833 C10.6929167,23.5216667 11.3025,23.5216667 11.8433333,23.2970833 C15.77125,21.6608333 22,16.0095833 22,5.86666667 C22,4.9775 21.46375,4.17541667 20.6479167,3.83625 L11.8479167,0.169583333 L11.8479166,0.169583316 C11.3065333,-0.0550036844 10.69805,-0.0550036844 10.1566666,0.169583351 L1.35666662,3.83625002 C0.536249957,4.17541668 -4.28210001e-08,4.97750002 -4.28210001e-08,5.86666668 C-4.28210001e-08,14.9645834 5.24791662,21.2529167 10.1520833,23.2970834 L10.1520833,23.2970833 Z M11,2.2 L19.8,5.86666667 C19.8,13.8325 15.29,19.4791667 11,21.2666667 C6.53125,19.4058333 2.2,13.62625 2.2,5.86666667 L11,2.2 Z M11,13 C12.6568542,13 14,11.6568542 14,10 C14,8.34314575 12.6568542,7 11,7 C9.34314575,7 8,8.34314575 8,10 C8,11.6568542 9.34314575,13 11,13 Z"
            />
        </SvgIcon>
    );
}

BadgeUnclaimed.defaultProps = {
    color: 'currentColor',
};

BadgeUnclaimed.propTypes = {
    color: string,
};
