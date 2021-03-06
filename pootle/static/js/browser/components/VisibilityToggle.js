/*
 * Copyright (C) Pootle contributors.
 *
 * This file is a part of the Pootle project. It is distributed under the GPL3
 * or later license. See the LICENSE file for a copy of the license and the
 * AUTHORS file for copyright and authorship information.
 */

import React, { PropTypes } from 'react';

import TextToggle from 'components/TextToggle';


const VisibilityToggle = React.createClass({

  propTypes: {
    // FIXME: read from context when it becomes available
    uiLocaleDir: PropTypes.string.isRequired,
  },

  componentDidMount() {
    this.handleVisibility({ isActive: false });
  },

  /**
   * Note this is coupled with the DOM and how the browsing table is rendered.
   * The implementation must change once the table is rendered as a component.
   */
  handleVisibility({ isActive: showDisabled }) {
    const rows = [...document.querySelectorAll('tr.item')];
    rows.map(row => row.classList.remove('odd'));
    rows
      .filter(row => row.classList.contains('is-disabled'))
      .forEach(row => row.classList.toggle('is-visible', showDisabled));

    [...document.querySelectorAll('tr.is-visible')].forEach((row, i) => {
      row.classList.toggle('odd', i % 2 === 0);
    });
  },

  render() {
    const style = {
      position: 'absolute',
      [this.props.uiLocaleDir === 'ltr' ? 'right' : 'left']: '2em',
      color: '#c30',
      zIndex: '2',
    };

    return (
      <TextToggle
        defaultChecked
        labelActive={gettext('Show disabled')}
        labelInactive={gettext('Hide disabled')}
        onClick={this.handleVisibility}
        style={style}
      />
    );
  },

});


export default VisibilityToggle;
