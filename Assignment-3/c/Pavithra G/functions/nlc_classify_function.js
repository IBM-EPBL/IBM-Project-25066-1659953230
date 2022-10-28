const assert = require('assert');
const NaturalLanguageClassifierV1 = require('watson-developer-cloud/natural-language-classifier/v1');

/**
  *
  * @param {Object} params - The parameters to send to the service.
  * @param {string} [params.username] - The username used to authenticate with the service. Username and password credentials are only required to run your application locally or outside of Bluemix. When running on Bluemix, the credentials will be automatically loaded from the `VCAP_SERVICES` environment variable.
  * @param {string} [params.password] - The password used to authenticate with the service. Username and password credentials are only required to run your application locally or outside of Bluemix. When running on Bluemix, the credentials will be automatically loaded from the `VCAP_SERVICES` environment variable.
  * @param {string} [params.iam_access_token] - An IAM access token fully managed by the application. Responsibility falls on the application to refresh the token, either before it expires or reactively upon receiving a 401 from the service, as any requests made with an expired token will fail.
  * @param {string} [params.iam_apikey] - An API key that can be used to request IAM tokens. If this API key is provided, the SDK will manage the token and handle the refreshing.
  * @param {string} [params.iam_url] - An optional URL for the IAM service API. Defaults to 'https://iam.bluemix.net/identity/token'.
  * @param {Object} [params.headers] - Custom HTTP request headers
  * @param {boolean} [params.headers.X-Watson-Learning-Opt-Out=false] - opt-out of data collection
  * @param {string} [params.url] - override default service base url
  * @param {string} params.classifier_id - Classifier ID to use.
  * @param {string} params.text - The submitted phrase. The maximum length is 2048 characters.
  * @return {Promise} - The Promise that the action returns.
  *
  */
function main(params) {
  return new Promise(function (resolve, reject) {

    let natural_language_classifier;

    natural_language_classifier = new NaturalLanguageClassifierV1({
      iam_apikey: params.iam_apikey,
      username: params.username,
      password: params.password,
      url: params.url
    });

    var nlc_request = {
      text: params.text,
      classifier_id: params.classifier_id
    };

    natural_language_classifier.classify(nlc_request, function (error, nlc_results) {
      if (error) {
        return reject(error);
      } else {
        return resolve(nlc_results);
      }
    });
  });
}
