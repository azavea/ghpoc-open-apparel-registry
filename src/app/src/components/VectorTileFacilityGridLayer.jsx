import React, { useEffect, useRef, useState } from 'react';
import { bool, func, number, string } from 'prop-types';
import { connect } from 'react-redux';
import VectorGridDefault from 'react-leaflet-vectorgrid';
import { withLeaflet } from 'react-leaflet';
import L from 'leaflet';
import get from 'lodash/get';

import {
    createQueryStringFromSearchFilters,
    createTileURLWithQueryString,
    createTileCacheKeyWithEncodedFilters,
} from '../util/util';

import { GRID_COLOR_RAMP } from '../util/constants';

const VectorGrid = withLeaflet(VectorGridDefault);

function useUpdateTileURL(tileURL, performingNewSearch, resetButtonClickCount) {
    const [
        vectorTileURLWithQueryParams,
        setVectorTileURLWithQueryParams,
    ] = useState(tileURL);

    const [isFetching, setIsFetching] = useState(performingNewSearch);
    const [storedResetCount, setStoredResetCount] = useState(
        resetButtonClickCount,
    );

    useEffect(() => {
        if (performingNewSearch && !isFetching) {
            setIsFetching(true);
        } else if (!performingNewSearch && isFetching) {
            setIsFetching(false);
            setVectorTileURLWithQueryParams(tileURL);
        } else if (resetButtonClickCount !== storedResetCount) {
            setIsFetching(false);
            setStoredResetCount(resetButtonClickCount);
            setVectorTileURLWithQueryParams(tileURL);
        }
    }, [
        tileURL,
        setVectorTileURLWithQueryParams,
        isFetching,
        setIsFetching,
        performingNewSearch,
        storedResetCount,
        setStoredResetCount,
        resetButtonClickCount,
    ]);

    return vectorTileURLWithQueryParams;
}

const VectorTileFacilityGridLayer = ({
    tileURL,
    fetching,
    resetButtonClickCount,
    tileCacheKey,
    getNewCacheKey,
    handleCellClick,
    minZoom,
    maxZoom,
}) => {
    const vectorTileURL = useUpdateTileURL(
        tileURL,
        fetching,
        resetButtonClickCount,
        getNewCacheKey,
    );

    const vectorTileLayerRef = useRef(null);

    if (!tileCacheKey) {
        // We throw an error here if the tile cache key is missing.
        // This crashes the map, intentionally, but an ErrorBoundary
        // handles the crash so that the application continues to run.
        throw new Error('Missing tile cache key');
    }

    return (
        <VectorGrid
            ref={vectorTileLayerRef}
            key={vectorTileURL}
            url={vectorTileURL}
            type="protobuf"
            rendererFactory={L.canvas.tile}
            updateWhenZooming={false}
            minZoom={minZoom}
            maxZoom={maxZoom}
            vectorTileLayerStyles={{
                facilitygrid(properties) {
                    const layer = get(
                        vectorTileLayerRef,
                        'current.leafletElement',
                    );
                    // eslint-disable-next-line no-underscore-dangle
                    const zoomLevel = layer._map.getZoom();
                    const factor = 2 * Math.max(0, zoomLevel - 4);
                    const count = get(properties, 'count', 0);
                    if (count === 0) {
                        return {
                            fill: false,
                            stroke: false,
                        };
                    }
                    const fillColor = GRID_COLOR_RAMP.reduce(
                        // eslint-disable-next-line no-confusing-arrow
                        (color, [val, c]) => count + factor > val ? c : color, GRID_COLOR_RAMP[0],
                    );

                    return {
                        fill: true,
                        fillColor,
                        fillOpacity: 0.8,
                        stroke: true,
                        weight: 0.5,
                        color: '#0427A4',
                    };
                },
            }}
            subdomains=""
            zIndex={100}
            interactive
            onClick={handleCellClick}
        />
    );
};

VectorTileFacilityGridLayer.propTypes = {
    handleCellClick: func.isRequired,
    tileURL: string.isRequired,
    tileCacheKey: string.isRequired,
    fetching: bool.isRequired,
    resetButtonClickCount: number.isRequired,
};

function mapStateToProps({
    filters,
    facilities: {
        facilities: { fetching },
    },
    ui: {
        facilitiesSidebarTabSearch: { resetButtonClickCount },
    },
    vectorTileLayer: {
        key,
    },
}) {
    const querystring = createQueryStringFromSearchFilters(filters);
    const tileCacheKey = createTileCacheKeyWithEncodedFilters(filters, key);
    const tileURL = createTileURLWithQueryString(querystring, tileCacheKey);

    return {
        tileURL,
        tileCacheKey,
        fetching,
        resetButtonClickCount,
    };
}

export default connect(
    mapStateToProps,
)(VectorTileFacilityGridLayer);