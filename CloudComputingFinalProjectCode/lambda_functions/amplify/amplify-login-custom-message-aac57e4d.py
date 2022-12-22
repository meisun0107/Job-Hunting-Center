"use strict";
exports.handler = async (event, context, callback) => {
    let appName;
    let appId;
    let appLink;
    let region;
    let environment;
    if (event.request.clientMetadata) {
        ({ appId, appName, appLink, region, environment } = event.request.clientMetadata);
    }
    let sanitizedAppName = appName ? appName.replace(/[^a-zA-Z0-9]/g, '') : '';
    if (sanitizedAppName.length < 3) {
        sanitizedAppName = 'amplify';
    }
    const inviteLink = region !== undefined && environment !== undefined
        ? `https://${region}.admin.amplifyapp.com/admin/login?appId=${appId}&backendEnvironmentName=${environment}`
        : appLink;
    const templateInvite = (email, code) => `<div style="margin: 0 auto; width: 600px; background-color: #fff; font-size: 1.2rem; font-style: normal; font-weight: normal; line-height: 19px;" align="center">
<div style="padding: 20;">
  <p style="margin-top: 20px; margin-bottom: 0px; font-size: 16px; line-height: 24px; color: #000000; text-align: left;">Hi!</p>
  <p style="margin-top: 20px; margin-bottom: 0px; font-size: 16px; line-height: 24px; color: #000000; text-align: left;">You are invited to collaborate on the ${sanitizedAppName} (${appId}) project on AWS Amplify.</p>
  <p style="margin-top: 20px; margin-bottom: 0px; font-size: 16px; line-height: 24px; color: #000000; text-align: left;">Your temporary credentials are:</p>
  <p style="margin-top: 0px; margin-bottom: 0px; font-size: 16px; line-height: 24px; color: #000000; text-align: left;"><strong>Username:</strong> <a style="text-decoration: none" href="mailto:${email}">${email}</a></p>
  <p style="margin-top: 0px; margin-bottom: 0px; font-size: 16px; line-height: 24px; color: #000000; text-align: left;"><strong>Temporary Password:</strong> ${code}</p>
  <p style="margin-top: 20px; margin-bottom: 0px; font-size: 16px; line-height: 24px; color: #000000; text-align: left;"><a style="text-decoration: none" href="${inviteLink}">Visit the Amplify Studio</a> to get started!</p>
</div>
</div>
`;
    if (event.triggerSource === 'CustomMessage_AdminCreateUser') {
        event.response = {
            emailSubject: 'Welcome to Amplify Studio | Your temporary account details',
            emailMessage: templateInvite(event.request.usernameParameter, event.request.codeParameter),
        };
    }
    callback(null, event);
    return event;
};
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiaW5kZXguanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyIuLi8uLi8uLi8uLi8uLi9zcmMvcGFja2FnZWRfanMvY29nbml0b190cmlnZ2Vyc19hcnRpZmFjdHMvYW1wbGlmeS1sb2dpbi1jdXN0b20tbWVzc2FnZS9pbmRleC5qcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiO0FBQUEsT0FBTyxDQUFDLE9BQU8sR0FBRyxLQUFLLEVBQUUsS0FBSyxFQUFFLE9BQU8sRUFBRSxRQUFRLEVBQUUsRUFBRTtJQUNuRCxJQUFJLE9BQU8sQ0FBQztJQUNaLElBQUksS0FBSyxDQUFDO0lBQ1YsSUFBSSxPQUFPLENBQUM7SUFDWixJQUFJLE1BQU0sQ0FBQztJQUNYLElBQUksV0FBVyxDQUFDO0lBQ2hCLElBQUksS0FBSyxDQUFDLE9BQU8sQ0FBQyxjQUFjLEVBQUU7UUFDaEMsQ0FBQyxFQUFFLEtBQUssRUFBRSxPQUFPLEVBQUUsT0FBTyxFQUFFLE1BQU0sRUFBRSxXQUFXLEVBQUUsR0FBRyxLQUFLLENBQUMsT0FBTyxDQUFDLGNBQWMsQ0FBQyxDQUFDO0tBQ25GO0lBRUQsSUFBSSxnQkFBZ0IsR0FBRyxPQUFPLENBQUMsQ0FBQyxDQUFDLE9BQU8sQ0FBQyxPQUFPLENBQUMsZUFBZSxFQUFFLEVBQUUsQ0FBQyxDQUFDLENBQUMsQ0FBQyxFQUFFLENBQUM7SUFDM0UsSUFBSSxnQkFBZ0IsQ0FBQyxNQUFNLEdBQUcsQ0FBQyxFQUFFO1FBQy9CLGdCQUFnQixHQUFHLFNBQVMsQ0FBQztLQUM5QjtJQUVELE1BQU0sVUFBVSxHQUNkLE1BQU0sS0FBSyxTQUFTLElBQUksV0FBVyxLQUFLLFNBQVM7UUFDL0MsQ0FBQyxDQUFDLFdBQVcsTUFBTSwyQ0FBMkMsS0FBSywyQkFBMkIsV0FBVyxFQUFFO1FBQzNHLENBQUMsQ0FBQyxPQUFPLENBQUM7SUFFZCxNQUFNLGNBQWMsR0FBRyxDQUNyQixLQUFLLEVBQ0wsSUFBSSxFQUNKLEVBQUUsQ0FBQzs7O2lLQUcwSixnQkFBZ0IsS0FBSyxLQUFLOzttTUFFUSxLQUFLLEtBQUssS0FBSzsrSkFDbkQsSUFBSTtrS0FDRCxVQUFVOzs7Q0FHM0ssQ0FBQztJQUNBLElBQUksS0FBSyxDQUFDLGFBQWEsS0FBSywrQkFBK0IsRUFBRTtRQUMzRCxLQUFLLENBQUMsUUFBUSxHQUFHO1lBQ2YsWUFBWSxFQUFFLDREQUE0RDtZQUMxRSxZQUFZLEVBQUUsY0FBYyxDQUFDLEtBQUssQ0FBQyxPQUFPLENBQUMsaUJBQWlCLEVBQUUsS0FBSyxDQUFDLE9BQU8sQ0FBQyxhQUFhLENBQUM7U0FDM0YsQ0FBQztLQUNIO0lBRUQsUUFBUSxDQUFDLElBQUksRUFBRSxLQUFLLENBQUMsQ0FBQztJQUN0QixPQUFPLEtBQUssQ0FBQztBQUNmLENBQUMsQ0FBQyJ9