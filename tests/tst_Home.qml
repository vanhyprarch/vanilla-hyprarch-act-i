// SPDX-License-Identifier: GPL-2.0-only
import QtQuick
import QtTest
import "../shell"

Item {
  width: 1280
  height: 720
  Home { id: home; anchors.fill: parent }
  TestCase {
    name: "HomeKeyboardNavigation"
    when: windowShown
    function init() {
      home.selectedIndex = 0;
      home.notice = "";
      home.forceActiveFocus();
      tryVerify(() => home.activeFocus);
    }
    function test_gamepad_navigation_and_modal_back() {
      home.navigate("previous");
      compare(home.selectedIndex, 1);
      home.navigate("select");
      verify(home.notice.indexOf("Moonlight") !== -1);
      home.navigate("next");
      compare(home.selectedIndex, 1);
      home.navigate("back");
      compare(home.notice, "");
      home.navigate("next");
      compare(home.selectedIndex, 0);
    }
    function test_arrow_navigation_wraps() {
      keyClick(Qt.Key_Right);
      compare(home.selectedIndex, 1);
      keyClick(Qt.Key_Right);
      compare(home.selectedIndex, 0);
      keyClick(Qt.Key_Left);
      compare(home.selectedIndex, 1);
    }
    function test_tab_and_backtab() {
      keyClick(Qt.Key_Tab);
      compare(home.selectedIndex, 1);
      keyClick(Qt.Key_Backtab);
      compare(home.selectedIndex, 0);
    }
    function test_selected_app_feedback_and_back() {
      keyClick(Qt.Key_Right);
      keyClick(Qt.Key_Return);
      verify(home.notice.indexOf("Moonlight") !== -1);
      keyClick(Qt.Key_Left);
      compare(home.selectedIndex, 1);
      keyClick(Qt.Key_Escape);
      compare(home.notice, "");
      compare(home.selectedIndex, 1);
    }
  }
}
