import React, { memo } from 'react';
import Grid from '@material-ui/core/Grid';

import AppGrid from './AppGrid';
import AppOverflow from './AppOverflow';

const AboutClaimedFacilities = memo(() => (
    <AppOverflow>
        <AppGrid title="How OAR Facility Claims Are Verified">
            <Grid container className="margin-bottom-64">
                <Grid item xs={12}>
                    <h2 id="introduction">
                        Introduction
                    </h2>
                    <p>
                        The Open Apparel Registry (OAR) enables facility owners
                        or managers to claim facilities. Once a facility claim
                        is verified by OAR staff, the facility claimant can add
                        information about the facility such as a description of
                        the facility, contact information, and production info
                        which is displayed publicly on the facility details page.
                    </p>
                    <h2 id="verification-process">
                        Verifying Facility Claims
                    </h2>
                    <p>
                        The process for verifying a facility claim is x, y, z.
                    </p>
                    <h2 id="disclaimer">
                        Disclaimer
                    </h2>
                    <p>
                        For verified facility claims, OAR staff has verified that
                        the claimant has a connection with the facility sufficient
                        to give the claimant access to updating details about the
                        facility. However, OAR staff does not verify each detail
                        the claimant subsequently adds about a facility.
                    </p>
                    <p>
                        If you believe that some claimed facility data is inaccurate
                        or incorrect, please send an email to{' '}
                        <a href="mailto:info@openapparel.org">
                            info@openapparel.org
                        </a> with a link to the facility details page and an explanation
                        of the problem.
                    </p>
                </Grid>
            </Grid>
        </AppGrid>
    </AppOverflow>
));

export default AboutClaimedFacilities;
