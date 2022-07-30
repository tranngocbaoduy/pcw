const AWS = require("aws-sdk");

AWS.config.update({
    credentials: new AWS.SharedIniFileCredentials({ profile: "pcw-admin" }),
    region: "ap-southeast-1",
});

/**
 * @param {AWS.DynamoDB.DocumentClient.QueryInput} params
 */
async function queryItems(params) {
    const dynamodbClient = new AWS.DynamoDB.DocumentClient();
    let result = null;
    result = await dynamodbClient
        .query(params)
        .promise()
        .then((i) => {
            // console.log(i);
            return i;
        });
    return result || [];
}

async function main() {
    const agencyItems = [];
    const brandItems = ["lg"];
    const PK = "WASHING";
    const limit = 12;
    const SK = null;
    const minPrice = 20000000;
    const maxPrice = 100000000;

    agencyValues = {};
    agencyFilterExpressionValues = [];
    agencyFilterExpressionNames = {};
    for (const agencyIndex in agencyItems) {
        agencyFilterExpressionValues.push(
            `begins_with(#DOMAIN, :domain${agencyIndex})`
        );
        agencyValues[`:domain${agencyIndex}`] = agencyItems[agencyIndex];
        agencyFilterExpressionNames["#DOMAIN"] = "domain";
    }

    brandValues = {};
    brandFilterExpressionValues = [];
    brandFilterExpressionNames = {};
    for (const brandIndex in brandItems) {
        brandFilterExpressionValues.push(
            `begins_with(#BRAND, :brand${brandIndex})`
        );
        brandValues[`:brand${brandIndex}`] = brandItems[brandIndex];
        brandFilterExpressionNames["#BRAND"] = "brand";
    }

    if (!PK) return [];
    const pasrams = {
        TableName: "pcw-duy-PRODUCT",
        KeyConditionExpression: "PK = :pk",
        FilterExpression: "begins_with(#DOMAIN, :domain) AND (price BETWEEN :minPrice AND :maxPrice)",
        // FilterExpression: `${brandFilterExpressionValues.length != 0
        //     ? `(${brandFilterExpressionValues.join(" OR ")}) AND`
        //     : ``
        //     } ${agencyFilterExpressionValues.length != 0
        //         ? `(${agencyFilterExpressionValues.join(" OR ")}) AND`
        //         : ``
        //     } (price BETWEEN :minPrice AND :maxPrice)`,
        ExpressionAttributeNames: {
            // "#SK": "SK",
            // "#BRAND": "brand",
            "#DOMAIN": "domain",
            // ...agencyFilterExpressionNames,
            // ...brandFilterExpressionNames
        },
        ExpressionAttributeValues: {
            ":pk": PK,
            // ":sk": "REP#",
            ":minPrice": minPrice,
            ":maxPrice": maxPrice,
            // ...agencyValues,
            // ...brandValues,
            // ":brand": 'LG',
            ":domain": "shopee",
        },
        // Limit: limit,
    };
    if (PK && SK && PK.length != 0 && SK.length != 0) {
        params["ExclusiveStartKey"] = {
            PK: PK,
            SK: SK,
        };
    }
    // console.log("params", params);
    //   params = {
    //     TableName: "pcw-duy-PRODUCT",
    //     KeyConditionExpression: "#PK = :pk",
    //     FilterExpression:
    //       " (begins_with(#DOMAIN, :domain0)) AND (price BETWEEN :minPrice AND :maxPrice)",
    //     ExpressionAttributeNames: { "#PK": "PK", "#DOMAIN": "domain" },
    //     ExpressionAttributeValues: {
    //       ":pk": "WASHING",
    //       ":minPrice": 0,
    //       ":maxPrice": 10000000,
    //       ":domain0": "dienmayxanh",
    //     },
    //   };
    params = {
        TableName: "pcw-duy-PRODUCT",
        KeyConditionExpression: "#PK = :pk",
        FilterExpression:
            " (begins_with(#DOMAIN, :domain0)) AND (price BETWEEN :minPrice AND :maxPrice)",
        ExpressionAttributeNames: { "#PK": "PK", "#DOMAIN": "domain" },
        ExpressionAttributeValues: {
            ":pk": "WASHING",
            ":minPrice": 0,
            ":maxPrice": 10000000,
            ":domain0": "dienmayxanh",
        },
    };
    const data = await queryItems(pasrams);
    console.log("data", data);
    console.log(data.Items.length)
}

main();
