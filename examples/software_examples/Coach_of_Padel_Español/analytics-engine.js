class AnalyticsEngine {

    /**
     * Recalculates risk indicators for a single user.
     * @param {object} user - The user object to analyze.
     * @returns {object} - The calculated risk factors for the user.
     */
    calculateRiskFactors(user) {
        if (!user.progressData) return user.riskFactors;

        const { adherenceHistory = [], performanceHistory = [], weightHistory = [] } = user.progressData;
        const riskFactors = {
            lastUpdate: Date.now(),
            adherenceScore: 0.5,
            progressScore: 0.5,
            engagementScore: 0.5,
            riskLevel: 'medium',
            predictedChurnDate: null
        };

        if (adherenceHistory.length > 0) {
            const lastFourWeeks = adherenceHistory.slice(-4);
            
            const workoutRatios = lastFourWeeks.map(week => {
                if (!week.workouts_planned || week.workouts_planned === 0) {
                    return 1;
                }
                return (week.workouts_completed || 0) / week.workouts_planned;
            });

            const totalRatio = workoutRatios.reduce((sum, ratio) => sum + ratio, 0);
            riskFactors.adherenceScore = totalRatio / lastFourWeeks.length;
        } else {
            riskFactors.adherenceScore = 0.5;
        }


        if (weightHistory.length >= 1 && user.benchmarkProfile && user.benchmarkProfile.initialWeight > 0 && user.benchmarkProfile.targetWeight > 0) {
            const lastWeight = weightHistory[weightHistory.length - 1].weight;
            const initialWeight = user.benchmarkProfile.initialWeight;
            const targetWeight = user.benchmarkProfile.targetWeight;

            if (targetWeight < initialWeight) {
                const totalGoal = initialWeight - targetWeight;
                const progressMade = initialWeight - lastWeight;
                riskFactors.progressScore = Math.max(0, Math.min(1, progressMade / totalGoal));
            } 
            else if (targetWeight > initialWeight) {
                const totalGoal = targetWeight - initialWeight;
                const progressMade = lastWeight - initialWeight;
                 if (totalGoal > 0) {
                    riskFactors.progressScore = Math.max(0, Math.min(1, progressMade / totalGoal));
                }
            }
            else {
                const difference = Math.abs(lastWeight - initialWeight);
                const maxAllowedDifference = initialWeight * 0.05; 
                riskFactors.progressScore = maxAllowedDifference > 0 ? Math.max(0, 1 - (difference / maxAllowedDifference)) : 1;
            }
        }

        const userMessages = (user.chatHistory || []).filter(msg => msg.role === 'user' && msg.timestamp);

        if (userMessages.length === 0) {
            riskFactors.engagementScore = 0.5; 
        } else {
            const lastMessageTimestamp = userMessages[userMessages.length - 1].timestamp;
            const daysSinceLastMessage = (Date.now() - lastMessageTimestamp) / (1000 * 60 * 60 * 24);

            if (daysSinceLastMessage <= 7) {
                riskFactors.engagementScore = 1.0; 
            } else if (daysSinceLastMessage <= 14) {
                riskFactors.engagementScore = 0.7;
            } else if (daysSinceLastMessage <= 30) {
                riskFactors.engagementScore = 0.4;
            } else {
                riskFactors.engagementScore = 0.1;
            }
        }
        
        const weightedScore = (riskFactors.adherenceScore * 0.4) + (riskFactors.progressScore * 0.3) + (riskFactors.engagementScore * 0.3);

        if (weightedScore > 0.75) riskFactors.riskLevel = 'low';
        else if (weightedScore < 0.4) riskFactors.riskLevel = 'high';
        else riskFactors.riskLevel = 'medium';

        if (riskFactors.riskLevel === 'high') {
            const churnDate = new Date();
            churnDate.setDate(churnDate.getDate() + 14);
            riskFactors.predictedChurnDate = churnDate.toISOString().split('T')[0];
        }

        user.riskFactors = riskFactors;
        return riskFactors;
    }


    /**
     * Performs a full recalculation of all analytics.
     * Now accepts db as a reference and modifies it, delegating I/O to the server.
     */
    runFullRecalculation(db) {
        console.log("Running full analytics recalculation in RAM...");
        if (!db) return;

        const { users } = db;

        if (!users || users.length === 0) {
            console.log("No users found, analytics recalculation skipped.");
            db.analytics = {
                lastCalculation: Date.now(),
                globalMetrics: {
                    totalClients: 0,
                    activeClients: 0,
                    averageAdherence: 0,
                    averageProgressRate: 0,
                    churnRate: 0
                },
                patterns: {},
                benchmarks: {}
            };
            return;
        }

        let totalClients = users.length;
        let activeClients = 0;
        let churnedClients = 0;
        let totalProgress = 0;
        let sumOfAverageAdherences = 0;

        users.forEach(user => {
            this.calculateRiskFactors(user);
            if (user.riskFactors.riskLevel !== 'high') {
                activeClients++;
            } else {
                churnedClients++;
            }
            totalProgress += user.riskFactors.progressScore || 0;

            const adherenceEntries = user.progressData?.adherenceHistory || [];
            if (adherenceEntries.length > 0) {
                const sumOfRatios = adherenceEntries.reduce((sum, entry) => {
                    if (entry.workouts_planned > 0) {
                        return sum + (entry.workouts_completed / entry.workouts_planned);
                    }
                    return sum;
                }, 0);
                const userAverageAdherence = sumOfRatios / adherenceEntries.length;
                sumOfAverageAdherences += userAverageAdherence;
            }
        });

        const averageAdherence = totalClients > 0 ? sumOfAverageAdherences / totalClients : 0;

        db.analytics = db.analytics || {};
        db.analytics.lastCalculation = Date.now();
        db.analytics.globalMetrics = {
            totalClients,
            activeClients,
            averageAdherence,
            averageProgressRate: totalClients > 0 ? totalProgress / totalClients : 0,
            churnRate: totalClients > 0 ? churnedClients / totalClients : 0
        };

        db.analytics.patterns = {
             successFactors: [ { factor: "Weekly check-ins", correlation: 0.78 } ],
             riskFactors: [ { factor: "3+ workouts missed", risk_multiplier: 2.4 } ]
        };
        db.analytics.benchmarks = {
            beginner_male_weight_loss: { avgWeightLossPerWeek: 0.7, avgAdherence: 0.75, avgDropoutWeek: 8 }
        };

        console.log("Full analytics recalculation completed.");
    }
}

module.exports = new AnalyticsEngine();
