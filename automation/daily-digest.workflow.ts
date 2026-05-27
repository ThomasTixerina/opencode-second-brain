import { workflow, node, links } from '@n8n-as-code/transformer';

// <workflow-map>
// Workflow : Daily Digest
// Nodes   : 3  |  Connections: 2
//
// NODE INDEX
// ──────────────────────────────────────────────────────────────────
// Property name                    Node type (short)         Flags
// ScheduleTrigger                    scheduleTrigger
// GenerateDailyPath                  code
// GithubReadDailyNote                github
//
// ROUTING MAP
// ──────────────────────────────────────────────────────────────────
// ScheduleTrigger
//    → GenerateDailyPath
//      → GithubReadDailyNote
// </workflow-map>

// =====================================================================
// METADATA DU WORKFLOW
// =====================================================================

@workflow({
    id: 'FNBEmCoMXY4FY5bD',
    name: 'Daily Digest',
    active: false,
    isArchived: false,
    settings: { executionOrder: 'v1' },
})
export class DailyDigestWorkflow {
    // =====================================================================
    // CONFIGURATION DES NOEUDS
    // =====================================================================

    @node({
        id: '4a4a63f6-8da2-4a93-bb13-80dcc228cdc6',
        name: 'Schedule Trigger',
        type: 'n8n-nodes-base.scheduleTrigger',
        version: 1.3,
        position: [250, 300],
    })
    ScheduleTrigger = {
        rule: {
            interval: [
                {
                    field: 'days',
                    daysInterval: 1,
                    triggerAtHour: 8,
                    triggerAtMinute: 0,
                },
            ],
        },
    };

    @node({
        id: 'aa49e3d4-1401-4705-924a-0cdac32e826c',
        name: 'Generate Daily Path',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [500, 300],
    })
    GenerateDailyPath = {
        language: 'javaScript',
        mode: 'runOnceForAllItems',
        jsCode: `const now = new Date();
const year = now.getFullYear();
const month = String(now.getMonth() + 1).padStart(2, '0');
const day = String(now.getDate()).padStart(2, '0');
const dateStr = \`\${year}-\${month}-\${day}\`;

return [
  {
    json: {
      dailyPath: \`daily/\${dateStr}.md\`,
      date: dateStr,
    },
  },
];`,
    };

    @node({
        id: '6f8e7dc4-4a57-4527-aac1-78828c231b08',
        webhookId: '8fb62461-1dac-4dd4-93f0-b0dc8c7f5ab8',
        name: 'GitHub - Read Daily Note',
        type: 'n8n-nodes-base.github',
        version: 1.1,
        position: [750, 300],
    })
    GithubReadDailyNote = {
        resource: 'file',
        operation: 'get',
        owner: {
            mode: 'name',
            value: 'ThomasTixerina',
        },
        repository: {
            mode: 'name',
            value: 'second-brain',
        },
        filePath: '={{ $json.dailyPath }}',
        asBinaryProperty: false,
        additionalParameters: {},
    };

    // =====================================================================
    // ROUTAGE ET CONNEXIONS
    // =====================================================================

    @links()
    defineRouting() {
        this.ScheduleTrigger.out(0).to(this.GenerateDailyPath.in(0));
        this.GenerateDailyPath.out(0).to(this.GithubReadDailyNote.in(0));
    }
}
