import { workflow, node, links } from '@n8n-as-code/transformer';

@workflow({
    id: 'tpkJQyuUcHqlXkdA',
    name: 'Vault Gateway',
    active: true,
    isArchived: false,
    settings: { executionOrder: 'v1' },
})
export class VaultGatewayWorkflow {
    @node({
        id: 'd47efdeb-7c99-4284-ac90-e48286d7f901',
        webhookId: '0c3ab153-6134-4ede-bba6-9866d04fb023',
        name: 'Webhook',
        type: 'n8n-nodes-base.webhook',
        version: 2.1,
        position: [256, 304],
    })
    Webhook = {
        httpMethod: 'POST',
        path: 'vault-gateway',
        responseMode: 'lastNode',
        options: {},
    };

    @node({
        id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
        name: 'Base64 Encode Content',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [430, 304],
    })
    Base64EncodeContent = {
        language: 'javaScript',
        mode: 'runOnceForAllItems',
        jsCode: `const items = $input.all().map(item => ({
  json: {
    path: item.json.body.path,
    content: Buffer.from(item.json.body.content).toString('base64'),
    commitMessage: item.json.body.commitMessage,
    sha: item.json.body.sha || undefined,
  },
}));
return items;`,
    };

    @node({
        id: '20f56c50-80f8-44dd-8ad5-5b28be2c99df',
        name: 'Create GitHub File',
        type: 'n8n-nodes-base.httpRequest',
        version: 4.4,
        position: [660, 304],
        credentials: { githubOAuth2Api: { id: 'gASlu5EsJ3zXmgNu', name: 'GitHub account' } },
    })
    CreateGitHubFile = {
        method: 'PUT',
        url: '=https://api.github.com/repos/ThomasTixerina/second-brain/contents/{{ $json.path }}',
        authentication: 'predefinedCredentialType',
        nodeCredentialType: 'githubOAuth2Api',
        sendBody: true,
        contentType: 'json',
        specifyBody: 'keypair',
        bodyParameters: {
            parameters: [
                {
                    name: 'message',
                    value: '={{ $json.commitMessage }}',
                },
                {
                    name: 'content',
                    value: '={{ $json.content }}',
                },
                {
                    name: 'sha',
                    value: '={{ $json.sha }}',
                },
            ],
        },
        options: {},
    };

    @links()
    defineRouting() {
        this.Webhook.out(0).to(this.Base64EncodeContent.in(0));
        this.Base64EncodeContent.out(0).to(this.CreateGitHubFile.in(0));
    }
}
