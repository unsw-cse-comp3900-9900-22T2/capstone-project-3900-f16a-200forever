import { notification } from "antd";

const openNotification = (msg) => {
  notification.open({
    message: msg["title"],
    description:
      msg["content"],
    placement: "top",
    duration: 3,
    onClick: () => {
      console.log("Notification Clicked!");
    },
  });
};

export default openNotification;
