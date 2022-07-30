export default class RouterHelper {
  static handleAsyncComponentError = (error: any): any => {
    console.error(error);
    window.alert('New version available! Please reload this page to continue.');
    window.location.reload();
  };
}
